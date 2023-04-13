#!/usr/bin/env python

import sys
import rospy
import numpy
import geometry_msgs.msg as geometry_msgs

from beginner_tutorials.srv import vectorInts

class ThrusterController:

	def __init__ (self):
	
		print('ThrusterController: initializing node')
		
		# geometry_msgs/Vector3.msg to represent Trust as a vector in free space
		self.pub_thruster = rospy.Publisher('thruster_trust', geometry_msgs.Vector3, queue_size=10)
		

	def handle_thruster(req):
	
		#Taking the request part of the message
		force = req.force
		torque = req.torque
		
		#Creating a vector with the information received 
		vector_force = numpy.array([req.force.x, req.force.y, req.force.z])
		vector_torque = numpy.array([req.torque.x, req.torque.y, req.torque.z])
		
		#Calculating the output
		thruster_output = (vector_force * vector_torque)
		
		#Publishing the in 
		thruster_thrust = geometry_msgs.Vector3()
		self.pub_thruster.publish(thruster_thrust)
	 
	 	return thruster_output
	
	def thruster_server():
	
		#Initializing the server
		rospy.init_node('thruster_server')
		s = rospy.Service('thruster', vectorInts, handle_thruster)
		print ("Calculating Thrust")
		rospy.spin()
		
		
if __name__ == '__main__':
	thruster_server()
		
	try:
		node = ThrusterController()
		
	except rospy.ROSInterruptException:
        	print('caught exception')
    	   print('exiting')