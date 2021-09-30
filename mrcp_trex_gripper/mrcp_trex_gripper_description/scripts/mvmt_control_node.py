#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import Float64
from roverv1.msg import rover_mvmt
# all necessary constants:
WIDTH_FRONT = 700
WIDTH_BACK  = 705.6
WIDTH = 700
LENGTH_FRONT_BACK = 793.89
LENGTH_FRONT_MIDDLE = 393.874
LENGTH_MIDDLE_BACK = 400.031
POINT_TURN_ANGLE = 0.8447394
wheel1 = rospy.Publisher('/roverv1/Motor1_velocity_controller/command', Float64, queue_size=10)
wheel2 = rospy.Publisher('/roverv1/Motor2_velocity_controller/command', Float64, queue_size=10)
wheel3 = rospy.Publisher('/roverv1/Motor3_velocity_controller/command', Float64, queue_size=10)
wheel4 = rospy.Publisher('/roverv1/Motor4_velocity_controller/command', Float64, queue_size=10)
wheel5 = rospy.Publisher('/roverv1/Motor5_velocity_controller/command', Float64, queue_size=10)
wheel6 = rospy.Publisher('/roverv1/Motor6_velocity_controller/command', Float64, queue_size=10)
servo1 = rospy.Publisher('/roverv1/Servo1_position_controller/command', Float64, queue_size=10)
servo2 = rospy.Publisher('/roverv1/Servo2_position_controller/command', Float64, queue_size=10)
servo3 = rospy.Publisher('/roverv1/Servo3_position_controller/command', Float64, queue_size=10)
servo4 = rospy.Publisher('/roverv1/Servo4_position_controller/command', Float64, queue_size=10)

def ackermann(speed, turn):
#--------------------------RIGHT TURN-----------------------------------------------------
	if turn >0:
	# right turn, front right servo has the largest angle. 
	#calculate radius from front right servo and apply it to all other wheels
		radius= (2*math.cos(turn*math.pi/180)*LENGTH_MIDDLE_BACK+math.sin(turn*math.pi/180)*WIDTH_BACK)/(2*math.sin(turn*math.pi/180))
		servoangle1 = math.atan(LENGTH_FRONT_MIDDLE/(radius+(WIDTH_FRONT/2)))*180/math.pi
		servoangle2 = math.atan(LENGTH_FRONT_MIDDLE/(radius-(WIDTH_FRONT/2)))*180/math.pi
		servoangle3 = math.atan(LENGTH_MIDDLE_BACK/(radius+(WIDTH_BACK/2)))*180/math.pi
		servoangle4 = math.atan(LENGTH_MIDDLE_BACK/(radius-(WIDTH_BACK/2)))*180/math.pi
		servo1.publish(-math.radians(servoangle1))
		servo2.publish(-math.radians(servoangle2))
		servo3.publish(math.radians(servoangle3))
		servo4.publish(math.radians(servoangle4))	

	# caclulate speed for each wheel
	# for right turn: rear left wheel has the highest speed.
	#calculate Radius for each wheel:
		radius1=math.sqrt(LENGTH_FRONT_MIDDLE*LENGTH_FRONT_MIDDLE+(radius+WIDTH_FRONT/2)*(radius+WIDTH_FRONT/2))
		radius2=math.sqrt(LENGTH_FRONT_MIDDLE*LENGTH_FRONT_MIDDLE+(radius-WIDTH_FRONT/2)*(radius-WIDTH_FRONT/2))
		radius3=radius+WIDTH/2
		radius4=radius-WIDTH/2		
		radius5=math.sqrt(LENGTH_MIDDLE_BACK*LENGTH_MIDDLE_BACK+(radius+WIDTH_BACK/2)*(radius+WIDTH_BACK/2))
		radius6=math.sqrt(LENGTH_MIDDLE_BACK*LENGTH_MIDDLE_BACK+(radius-WIDTH_BACK/2)*(radius-WIDTH_BACK/2))
	#calculate factor for each wheel: 		
		factor1=radius1/radius5
		factor2=radius2/radius5
		factor3=radius3/radius5
		factor4=radius4/radius5
		factor5=1
		factor6=radius6/radius5
	#convert speed from procent to actual value
		x= speed*0.04
	#publisch speed to each wheel including factor:
		wheel1.publish(x*factor1)
		wheel2.publish(-x*factor2)
		wheel3.publish(x*factor3)
		wheel4.publish(-x*factor4)
		wheel5.publish(x*factor5)
		wheel6.publish(-x*factor6)
#--------------------------LEFT TURN---------------------------------------------------------------
	elif turn <0:
	# left turn, front left servo has the largest angle. 
	#calculate radius from front left servo and apply it to all other wheels
		radius= (2*math.cos(abs(turn)*math.pi/180)*LENGTH_MIDDLE_BACK+math.sin(abs(turn)*math.pi/180)*WIDTH_BACK)/(2*math.sin(abs(turn)*math.pi/180))
		servoangle1 = math.atan(LENGTH_FRONT_MIDDLE/(radius-(WIDTH_FRONT/2)))*180/math.pi
		servoangle2 = math.atan(LENGTH_FRONT_MIDDLE/(radius+(WIDTH_FRONT/2)))*180/math.pi
		servoangle3 = math.atan(LENGTH_MIDDLE_BACK/(radius-(WIDTH_BACK/2)))*180/math.pi
		servoangle4 = math.atan(LENGTH_MIDDLE_BACK/(radius+(WIDTH_BACK/2)))*180/math.pi
		servo1.publish(math.radians(servoangle1))
		servo2.publish(math.radians(servoangle2))
		servo3.publish(-math.radians(servoangle3))
		servo4.publish(-math.radians(servoangle4))
	# caclulate speed for each wheel
	# for left turn: rear left wheel has the highest speed.
	#calculate Radius for each wheel:
		radius1=math.sqrt(LENGTH_FRONT_MIDDLE*LENGTH_FRONT_MIDDLE+(radius-WIDTH_FRONT/2)*(radius-WIDTH_FRONT/2))
		radius2=math.sqrt(LENGTH_FRONT_MIDDLE*LENGTH_FRONT_MIDDLE+(radius+WIDTH_FRONT/2)*(radius+WIDTH_FRONT/2))
		radius3=radius-WIDTH/2
		radius4=radius+WIDTH/2			
		radius5=math.sqrt(LENGTH_MIDDLE_BACK*LENGTH_MIDDLE_BACK+(radius-WIDTH_BACK/2)*(radius-WIDTH_BACK/2))	
		radius6=math.sqrt(LENGTH_MIDDLE_BACK*LENGTH_MIDDLE_BACK+(radius+WIDTH_BACK/2)*(radius+WIDTH_BACK/2))
		#calculate factor for each wheel: 			
		factor1=radius1/radius6
		factor2=radius2/radius6
		factor3=radius3/radius6
		factor4=radius4/radius6
		factor5=radius5/radius6
		factor6=1
	#convert speed from procent to actual value
		x= speed*0.04
	#publisch speed to each wheel including factor:
		wheel1.publish(x*factor1)
		wheel2.publish(-x*factor2)
		wheel3.publish(x*factor3)
		wheel4.publish(-x*factor4)
		wheel5.publish(x*factor5)
		wheel6.publish(-x*factor6)

def pointturn(speed):
	#set servos to specific angle
	servo1.publish(-POINT_TURN_ANGLE)
	servo2.publish(POINT_TURN_ANGLE)
	servo3.publish(POINT_TURN_ANGLE)
	servo4.publish(-POINT_TURN_ANGLE)
	#publish to wheels 
	x = speed*0.04
	wheel1.publish(x)
	wheel2.publish(x)
	wheel3.publish(x)
	wheel4.publish(x)
	wheel5.publish(x)
	wheel6.publish(x)
	return

def normal(speed):
	# set servos to 0 degree
	servo1.publish(0)
	servo2.publish(0)
	servo3.publish(0)
	servo4.publish(0)
	# publish speed to all wheels 
	x = speed*0.04
	wheel1.publish(x)
	wheel2.publish(-x)
	wheel3.publish(x)
	wheel4.publish(-x)
	wheel5.publish(x)
	wheel6.publish(-x)

	return

def callback(data):
	if data.mode == 'n':
		normal(data.speed)
	elif data.mode == 'a' and data.angle != 0:
		ackermann(data.speed,data.angle)
	elif data.mode == 'p':
		pointturn(data.speed)
	elif data.mode ==  'a' and data.angle == 0:
		normal(data.speed)
	return

if __name__=="__main__":
	try:
		rospy.init_node('rover_control_node')
		rospy.Subscriber('/roverv1/control', rover_mvmt, callback)
		rospy.spin()

	except rospy.ROSInterruptException:
		pass
