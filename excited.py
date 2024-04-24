commandExcited = [{'joint': 'joint_lift', 'delta': 0.2},{'joint': 'joint_head_pan', 'delta': 0.8},{'joint': 'joint_lift', 'delta': 0.8},{'joint': 'joint_wrist_yaw', 'delta': 0.8}] #self.keys.get_command(self)
duration=0.7

for i in range(len(commandExcited)-1):
    command=commandExcited[i]
    nextCommand=commandExcited[i+1]
    joint=command['joint']
    nextjoint=nextCommand['joint']
    if (joint!=nextjoint):
        rospy.loginfo(command)
        node.send_command(command, duration)
        rate.sleep()
    else: 
        rospy.loginfo(command)
        node.send_command(command, duration)
        rate.sleep()
        rate.sleep()
        rate.sleep()
        rate.sleep()
        rate.sleep()
        rate.sleep()
command= commandExcited[len(commandExcited)-1]
rate.sleep()
rate.sleep()
rate.sleep()
rate.sleep()
rate.sleep()
rate.sleep()
rospy.loginfo(command)
node.send_command(command, duration)
i=1
for i in range (0,50):
    rate.sleep()
    i=i+1

