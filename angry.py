commandAngry = [{'joint': 'joint_head_pan', 'delta': 0.2},{'joint': 'joint_lift', 'delta': 0.8},{'joint': 'joint_wrist_yaw', 'delta': 0.4},{'joint': 'joint_head_tilt', 'delta': -0.3}] #self.keys.get_command(self)
duration=0.7

for i in range(len(commandAngry)-1):
    command=commandExcited[i]
    nextCommand=commandExcited[i+1]
    joint=command['joint']
    nextjoint=nextCommand['joint']
    if (joint!=nextjoint):
        rospy.loginfo(command)
        node.send_command(command, duration)
    else: 
        rospy.loginfo(command)
        node.send_command(command, duration)
command= commandAngry[len(commandAngry)-1]
rospy.loginfo(command)
node.send_command(command, duration)
i=1
for i in range (0,50):
    rate.sleep()
    i=i+1

rate.sleep()
