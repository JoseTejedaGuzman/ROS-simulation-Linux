#!/usr/bin/env python 

#Importing geometry_msg libraries to use messages

import rospy
import numpy

from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import Wrench


""" Reading from the keyboard and publishing to 
uuv_gazebo/rexrov_wrench_control.launch through
---------------------------
Moving around:

   u    i    o
   j    k    l
   m    ,    .
   
---------------------------
   U    I    O
   J    K    L
   M    <    >
   
t : up (+z)
b : down (-z)

anything else : stop

CTRL-C to kill rosrun """

moveBindings = {
        'i':(1,0,0,0),
        'o':(1,0,0,-1),
        'j':(0,0,0,1),
        'l':(0,0,0,-1),
        'u':(1,0,0,1),
        ',':(-1,0,0,0),
        '.':(-1,0,0,1),
        'm':(-1,0,0,-1),
        'O':(1,-1,0,0),
        'I':(1,0,0,0),
        'J':(0,1,0,0),
        'L':(0,-1,0,0),
        'U':(1,1,0,0),
        '<':(-1,0,0,0),
        '>':(-1,-1,0,0),
        'M':(-1,1,0,0),
        't':(0,0,1,0),
        'b':(0,0,-1,0),
    }


#Creating node

class SimilarTeleopTwistNode:
	
	#Defining functions and their parameters
	
	def __init__(self):
		
		print('SimilarTeleopNode: initializing node')
		
		#Creating the publisher and subscriber parts of the node, where topic and type-message are specified
		
		self.subscribe_accel= rospy.Subscriber('cmd_accel', numpy_msg(Accel), self.accel_callback)
		self.publish_force = rospy.Publisher('thruster_manager/input', Wrench, queue_size=1)	
		self.x = 0.0
        	self.y = 0.0
        	self.z = 0.0
        	self.speed = 0.0
		
	def accel_callback (self, msg):
	
		#Calculating force and torque based on the information received by the node 'cmd_accel'
		#Angular and linear velocity are necesary to calculate the final force
		
		 force = numpy.array((msg.accel.linear.x, msg.accel.linear.y, msg.accel.linear.z))
		 
        	 torque = numpy.array((msg.accel.angular.x, msg.accel.angular.y, msg.accel.angular.z))
        	 
        	 #Stack force and torque vector
        	 force_torque = numpy.hstack((force, torque)).transpose()

		 #Allocating the values into the force_msg
        	 force_msg = Wrench()
        	 force_msg.force.x = force[0]
        	 force_msg.force.y = force[1]
        	 force_msg.force.z = force[2]

        	 force_msg.torque.x = torque[0]
        	 force_msg.torque.y = torque[1]
        	 force_msg.torque.z = torque[2]

		 #Publishing the values
        	 self.publish_force.publish(force_msg)
        	 
        def twist_run (self):
        
        	wrench_msg = WrenchMsg()

        	if stamped:
            		wrench = wrench_msg.wrench
            		wrench_msg.header.stamp = rospy.Time.now()
            		wrench_msg.header.frame_id = wrench_frame
       	else:
            		wrench = wrench_msg
       	while not self.done:
            		if stamped:
                		wrench_msg.header.stamp = rospy.Time.now()
           			self.condition.acquire()
           		
            			# Waiting for a new message 
            			self.condition.wait(self.timeout)

            			# Allocating the actual state into wrench message.
            			wrench.force.x = self.x * self.speed
            			wrench.force.y = self.y * self.speed
            			wrench.force.z = self.z * self.speed
            			wrench.torque.x = 0
            			wrench.torque.y = 0
            			wrench.torque.z = 0

            			self.condition.release()
            			
            			self.publish_force.publish(wrench_msg)	
	
  if __name__ == '__main__':
  
  	settings = saveTerminalSettings()
  
    	print('starting similar_teleop_twist.py')
    	rospy.init_node('similar_twist')
    	
    	#Creating values based on the parameter call
    	key_timeout = rospy.get_param("~key_timeout", 0.5)
    	twist_frame = rospy.get_param("~frame_id", '')

    	try:
        	node = SimilarTeleopTwistNode()
        	rospy.spin()
        	
        	while(1):
        	
        		#Receiving the input from the keyboard
            		key = getKey(settings, key_timeout)
            		#If a valid key is given
            		if key in moveBindings.keys():
            		
                		x = moveBindings[key][0]
                		y = moveBindings[key][1]
                		z = moveBindings[key][2]
                		
                	else:
                		
                	#If the user stops the input, neutral state	
                	if key == '' and x == 0 and y == 0 and z == 0:
                    		continue
               			 x = 0
                			 y = 0
                			 z = 0
               	#Escaping character
                       if (key == '\x03'):
                       	break     		
    	except rospy.ROSInterruptException: