# Imports
## standard libraries
import math
import keyboard as kb
## ROS libraries
import rospy
from sensor_msgs.msg import JointState
from control_msgs.msg import FollowJointTrajectoryGoal, FollowJointTrajectoryAction
from trajectory_msgs.msg import JointTrajectoryPoint
from geometry_msgs.msg import Twist
import actionlib


class Sender():

    def __init__(self):
        self.rate = 10
        self.joint_state = None
        self.twist = Twist()
        self.dex_wrist_control = False
        
        rospy.loginfo('Ready!')
        
    def joint_states_callback(self, joint_state):
        self.joint_state = joint_state

    def send_command(self, command, dur):
        joint_state = self.joint_state
        self.trajectory_client_selector(command)
        if (joint_state is not None) and (command is not None):
            if 'translate_mobile_base' == command['joint'] or 'rotate_mobile_base' == command['joint']:
                self.cmd_vel_pub.publish(self.twist)
                return 0
            point = JointTrajectoryPoint()
            point.time_from_start = rospy.Duration(dur)
            trajectory_goal = FollowJointTrajectoryGoal()
            trajectory_goal.goal_time_tolerance = rospy.Time(1.0)

            joint_name = command['joint']
            if joint_name in ['joint_lift', 'joint_wrist_yaw', 'joint_wrist_roll', 'joint_wrist_pitch', 'joint_head_pan', 'joint_head_tilt']:
                trajectory_goal.trajectory.joint_names = [joint_name]
                joint_index = joint_state.name.index(joint_name)
                joint_value = joint_state.position[joint_index]
                delta = command['delta']
                new_value = joint_value + delta
                point.positions = [new_value]
            elif joint_name in ["joint_gripper_finger_left", "wrist_extension"]:
                if joint_name == "joint_gripper_finger_left":
                    trajectory_goal.trajectory.joint_names = ['joint_gripper_finger_left', 'joint_gripper_finger_right']
                else:
                    trajectory_goal.trajectory.joint_names = ['joint_arm_l0','joint_arm_l1', 'joint_arm_l2', 'joint_arm_l3']
                positions = []
                for j_name in trajectory_goal.trajectory.joint_names:
                    joint_index = joint_state.name.index(j_name)
                    joint_value = joint_state.position[joint_index]
                    delta = command['delta']
                    new_value = joint_value + delta/len(trajectory_goal.trajectory.joint_names)
                    positions.append(new_value)
                point.positions = positions

            trajectory_goal.trajectory.points = [point]
            trajectory_goal.trajectory.header.stamp = rospy.Time.now()
            if self.trajectory_client:
                self.trajectory_client.send_goal(trajectory_goal)
                # self.trajectory_client.wait_for_result()

    def trajectory_client_selector(self, command):
        self.trajectory_client = None
        self.twist.linear.x = 0
        self.twist.angular.z = 0
        try:
            joint = command['joint']
            if joint == 'joint_lift' or joint == 'joint_wrist_yaw' or joint == 'wrist_extension':
                self.trajectory_client = self.trajectory_arm_client
            if joint == 'joint_head_pan' or joint == 'joint_head_tilt':
                self.trajectory_client = self.trajectory_head_client
            if joint == 'joint_gripper_finger_right' or joint == 'joint_gripper_finger_left':
                self.trajectory_client = self.trajectory_gripper_client
            if self.dex_wrist_control:
                if joint == 'joint_wrist_roll' or joint == 'joint_wrist_pitch':
                    self.trajectory_client = self.trajectory_dex_wrist_client
            if joint == 'translate_mobile_base' or joint == 'rotate_mobile_base':
                if joint == 'translate_mobile_base':
                    if 'inc' in command:
                        self.twist.linear.x = command['inc']
                    else:
                        self.twist.linear.x = command['delta']
                else:
                    if 'inc' in command:
                        self.twist.angular.z = command['inc']
                    else:
                        self.twist.angular.z = command['delta']
        except TypeError:
            0

        
rospy.init_node('message_sender', anonymous=True)
dex_wrist_control = False

node = Sender()

node.trajectory_gripper_client = actionlib.SimpleActionClient('/stretch_gripper_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
server_reached = node.trajectory_gripper_client.wait_for_server(timeout=rospy.Duration(60.0))

node.trajectory_head_client = actionlib.SimpleActionClient('/stretch_head_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
server_reached = node.trajectory_head_client.wait_for_server(timeout=rospy.Duration(60.0))

node.trajectory_arm_client = actionlib.SimpleActionClient('/stretch_arm_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
server_reached = node.trajectory_arm_client.wait_for_server(timeout=rospy.Duration(60.0))

node.cmd_vel_pub = rospy.Publisher('/stretch_diff_drive_controller/cmd_vel', Twist, queue_size=10)

rospy.Subscriber('/joint_states', JointState, node.joint_states_callback)

rate = rospy.Rate(node.rate)

delta_rad = 6.0 * math.pi/180 #sm: 3.0, med: 6.0, lg: 12.0
delta_translate = 0.04 #sm: 0.005, med: 0.04, lg: 0.06

def sad():
    sad_command = [{'joint': 'joint_lift', 'delta': -0.4}, {'joint': 'joint_head_tilt', 'delta': -0.3}, {'joint': 'wrist_extension', 'delta': -0.5}]
    sad_command_restore = [{'joint': 'joint_lift', 'delta': 0.4}, {'joint': 'joint_head_tilt', 'delta': 0.3}, {'joint': 'wrist_extension', 'delta': 0.5}]

    dur = 0.85
    for ind in range(len(sad_command)-1):
        curr_cmd = sad_command[ind]
        nxt_cmd = sad_command[ind+1]
        curr_joint = curr_cmd['joint']
        nxt_joint = nxt_cmd['joint']
        if (curr_joint != nxt_joint):
            rate.sleep()
            rate.sleep()
            rate.sleep()
            rospy.loginfo(curr_cmd)
            node.send_command(curr_cmd, dur)
        else:
            rospy.loginfo(curr_cmd)
            node.send_command(curr_cmd, dur)
            rate.sleep()
            rate.sleep()
            rate.sleep()
            rate.sleep()
            rate.sleep()
    cmd = sad_command[len(sad_command)-1]
    rospy.loginfo(cmd)
    node.send_command(cmd, dur) 
    # move back
    rate.sleep() # how to control sleep time??
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    dur = 0.8
    for ind in range(len(sad_command_restore)-1):
        curr_cmd = sad_command_restore[ind]
        nxt_cmd = sad_command_restore[ind+1]
        curr_joint = curr_cmd['joint']
        nxt_joint = nxt_cmd['joint']
        if (curr_joint != nxt_joint):
            rospy.loginfo(curr_cmd)
            node.send_command(curr_cmd, dur)
        else:
            rospy.loginfo(curr_cmd)
            node.send_command(curr_cmd, dur)
            rate.sleep()
            rate.sleep()
            rate.sleep()
            rate.sleep()
            rate.sleep()
    cmd = sad_command_restore[len(sad_command_restore)-1]
    rospy.loginfo(cmd)
    node.send_command(cmd, dur)

def happy():
    happy_command = [{'joint': 'joint_lift', 'delta': 0.2}, {'joint': 'joint_head_pan', 'delta': 0.5}, {'joint': 'joint_lift', 'delta': -0.2}, 
                    {'joint': 'joint_head_pan', 'delta': -0.5}, {'joint': 'joint_lift', 'delta': 0.2}, {'joint': 'joint_head_pan', 'delta': 0.5}, 
                    {'joint': 'joint_lift', 'delta': -0.2}, {'joint': 'joint_head_pan', 'delta': -0.5}, {'joint': 'wrist_extension', 'delta': 0.4}]
    happy_command_rev = [{'joint': 'wrist_extension', 'delta':-0.4}]

    dur = 0.15
    for ind in range(len(happy_command)-1):
        curr_cmd = happy_command[ind]
        nxt_cmd = happy_command[ind+1]
        curr_joint = curr_cmd['joint']
        nxt_joint = nxt_cmd['joint']
        if (curr_joint != nxt_joint):
            rospy.loginfo(curr_cmd)
            node.send_command(curr_cmd, dur)
            rate.sleep()
            rate.sleep()
            rate.sleep()
        else:
            rospy.loginfo(curr_cmd)
            node.send_command(curr_cmd, dur)
            rate.sleep()
            rate.sleep()
            rate.sleep()
            rate.sleep()
            rate.sleep()
    cmd = happy_command[len(happy_command)-1]
    rospy.loginfo(cmd)
    node.send_command(cmd, dur)

    # move back
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    dur = 0.4
    for ind in range(len(happy_command_rev)-1):
        curr_cmd = happy_command_rev[ind]
        nxt_cmd = happy_command_rev[ind+1]
        curr_joint = curr_cmd['joint']
        nxt_joint = nxt_cmd['joint']
        if (curr_joint != nxt_joint):
            rospy.loginfo(curr_cmd)
            node.send_command(curr_cmd, dur)
            rate.sleep(1.0)
        else:
            rospy.loginfo(curr_cmd)
            node.send_command(curr_cmd, dur)
            rate.sleep()
    cmd = happy_command_rev[len(happy_command_rev)-1]
    rospy.loginfo(cmd)
    node.send_command(cmd, dur)

def angry():
    duration = 0.1
    commandAngry = [{'joint':'joint_head_pan','delta': 0.2}, {'joint': 'joint_lift', 'delta': 0.5}, {'joint': 'joint_wrist_yaw', 'delta': 0.5},
                   {'joint': 'wrist_extension', 'delta': 0.5}, {'joint': 'joint_head_tilt', 'delta': -0.3}]
    angry_rev = [{'joint':'joint_head_pan','delta': -0.2}, {'joint': 'joint_lift', 'delta': -0.5}, {'joint': 'joint_wrist_yaw', 'delta': -0.5},
                 {'joint': 'wrist_extension', 'delta': -0.5}, {'joint': 'joint_head_tilt', 'delta': 0.3}]
    for i in range(len(commandAngry)-1):
        command=commandAngry[i]
        nextCommand=commandAngry[i+1]
        joint=command['joint']
        nextjoint=nextCommand['joint']
        if (joint!=nextjoint):
            rospy.loginfo(command)
            node.send_command(command, duration)
            rate.sleep()
        else: 
            rospy.loginfo(command)
            node.send_command(command, duration)
            rate.sleep(0.8)
    command= commandAngry[len(commandAngry)-1]
    rospy.loginfo(command)
    node.send_command(command, duration)

    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()

    dur2 = 0.4
    for ind in range(len(angry_rev)-1):
        curr_cmd = angry_rev[ind]
        nxt_cmd = angry_rev[ind+1]
        curr_joint = curr_cmd['joint']
        nxt_joint = nxt_cmd['joint']
        if (curr_joint != nxt_joint):
            rospy.loginfo(curr_cmd)
            node.send_command(curr_cmd, dur2)
        else:
            rospy.loginfo(curr_cmd)
            node.send_command(curr_cmd, dur2)
            rate.sleep(0.8)
    cmd = angry_rev[len(angry_rev)-1]
    rospy.loginfo(cmd)
    node.send_command(cmd, dur2)
    rate.sleep()

def surprise():
    commandSurprise = [{'joint': 'joint_lift', 'delta': 0.2}, {'joint': 'joint_head_pan', 'delta': 0.5},
                      {'joint': 'joint_lift', 'delta': 0.2}, {'joint': 'joint_wrist_yaw', 'delta': 0.6}]
    surprise_rev = [{'joint': 'joint_lift', 'delta': -0.2}, {'joint': 'joint_head_pan', 'delta': -0.5},
                    {'joint': 'joint_lift', 'delta': -0.2}, {'joint': 'joint_wrist_yaw', 'delta': -0.6}]
    duration=0.7

    for i in range(len(commandSurprise)-1):
        command=commandSurprise[i]
        nextCommand=commandSurprise[i+1]
        joint=command['joint']
        nextjoint=nextCommand['joint']
        if (joint!=nextjoint):
            rospy.loginfo(command)
            node.send_command(command, duration)
            rate.sleep()
            rate.sleep()
        else:
            rospy.loginfo(command)
            node.send_command(command, duration)
            rate.sleep()
            rate.sleep()
            rate.sleep()
            rate.sleep()
    command= commandSurprise[len(commandSurprise)-1]
    rospy.loginfo(command)
    node.send_command(command, duration)

    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()
    rate.sleep()

    dur2 = 0.4
    for ind in range(len(surprise_rev)-1):
        curr_cmd = surprise_rev[ind]
        nxt_cmd = surprise_rev[ind+1]
        curr_joint = curr_cmd['joint']
        nxt_joint = nxt_cmd['joint']
        if (curr_joint != nxt_joint):
            rospy.loginfo(curr_cmd)
            node.send_command(curr_cmd, dur2)
        else:
            rospy.loginfo(curr_cmd)
            node.send_command(curr_cmd, dur2)
            rate.sleep(0.8)
    cmd = surprise_rev[len(surprise_rev)-1]
    rospy.loginfo(cmd)
    node.send_command(cmd, dur2)
    rate.sleep()

# sad()
# rate.sleep()
# rate.sleep()
# happy()
# surprise()

# for restoring movements
rate.sleep()
rate.sleep()
rate.sleep()
rate.sleep()
rate.sleep()
cmd = {'joint': 'joint_lift', 'delta': 0.1}
# cmd2 = {'joint': 'wrist_extension', 'delta': 0.1}
rospy.loginfo(cmd)
node.send_command(cmd, 0.1)