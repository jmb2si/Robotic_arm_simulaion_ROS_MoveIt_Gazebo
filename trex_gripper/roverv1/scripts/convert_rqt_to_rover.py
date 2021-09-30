#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import Float64
from roverv1.msg import rover_mvmt
from geometry_msgs.msg import Twist

def callback(data):
	
	message.speed = data.linear.x*100
	message.angle = data.angular.z*-30
	if data.angular.z == 0:
		message.mode = 'n'
	elif data.angular.z != 0:
		message.mode = 'a'
	pub.publish(message)

	return

if __name__=="__main__":
	try:
		rospy.init_node('convert_rqt_to_rover')
		rospy.Subscriber('/cmd_vel', Twist, callback)
		pub = rospy.Publisher('/roverv1/control', rover_mvmt, queue_size = 5)
		message = rover_mvmt()
		rospy.spin()

	except rospy.ROSInterruptException:
		pass
