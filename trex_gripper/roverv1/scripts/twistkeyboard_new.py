#!/usr/bin/env python
from __future__ import print_function
import tty
import termios
import select
from roverv1.msg import rover_mvmt
import sys
from std_msgs.msg import Float64
import math
import rospy
import roslib
roslib.load_manifest('teleop_twist_keyboard')

msg = """
Reading from the keyboard  and Publishing to roverv1/control!
---------------------------
Moving around:
       i    
  j    k    l
       ,    
q/y : increase/decrease max speeds by 10%
change drive mode:
a : ackermann
p : point turn 
n : normal 

CTRL-C to quit
"""
moveBindings = {
		'i':'i',
		'j':'j',
		'l':'l',
		',':',',
		'k':'k',
	       }

speedBindings={
		'q':'q',
		'y':'y',
		'h':'h',
	      }
movementBindings={
		'p':'p',
		'a':'a',
		'n':'n',
	      }

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

def vels(speed,turn,message):
	return "currently:\tspeed:  %s Procent\tturn: %s Degree     \tmode: %s " % (speed,turn, message)

if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)
	pub = rospy.Publisher('/roverv1/control', rover_mvmt, queue_size = 1)
	rospy.init_node('rover_keyboard')
	drivemode = 'n'
	speed = 0
	turn = 0
	message = rover_mvmt()

	try:
		print(msg)
		message.mode = 'n'
		print(vels(speed,turn,message.mode))
		while(1):
			key = getKey()
			
			if key in moveBindings.keys():
				if key == 'k':
					message.speed = 0
				elif key == 'i':
					message.speed = speed
				elif key == ',':
					message.speed = -speed
				elif key == 'l':
					if turn <= 55:
						turn = turn +5
					message.angle = turn
				elif key == 'j':
					if turn >= -55:
						turn = turn-5
					message.angle = turn	
				print(vels(speed,turn,message.mode))

			elif key in speedBindings.keys():
				if key == 'q':
					if speed <= 90:
						speed = speed +10
				elif key == 'y':
					if speed >=10:
						speed = speed -10
				elif key == 'h':
					print(msg)

				print(vels(speed,turn,message.mode))


			elif key in movementBindings.keys():
				
				if key == 'n':
					print("Drive mode changed to normal")
					message.mode = 'n'
				elif key == 'p':
					print("Drive mode changed to point turn")
					message.mode = 'p'	
				elif key == 'a':
					print("Mode changed to ackermann drive")
					message.mode = 'a'
					



			else:
				print("Unknown key, press h for a list of availeble keys")

				if (key == '\x03'):
					break
			pub.publish(message)
#end 

	except Exception as e:print(e)

	finally:termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
