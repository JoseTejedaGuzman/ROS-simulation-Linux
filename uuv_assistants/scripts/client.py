!/usr/bin/env python

import sys
import rospy
from uuv_assistants.srv import *

def thruster_client(force, torque):
	#Calling the server
	rospy.wait_for_service('thruster_thrust')
	try:
		thruster_thrust = rospy.ServiceProxy('thruster_thrust', vectorInts)
		req = vectorIntsRequest()
		req.force = force
		req.torque = torque
		resp1 = thruster_thrust(req)
		return resp1.thruster_output
	except rospy.ServiceException as e:
		print("Service call failed: %s" %e)
		
if __name__ == "__main__":
	if len(sys.argv) == 3
		force = float(sys.argv[1.0])
		torque = float(sys.argv[2.0])
	
	else:
		#Publish the thrust force
		print("Thruster_client.py")
		sys.exit(1)
		print("Thrust = %s"%(thruster_client(force, torque))