import dvrk
import numpy
import PyKDL
import math


def check_angle_um(angle):
	if radian:
		return angle
	return (angle * math.pi) / 180

def check_angle_um_to_deg(angle):
	if radian:
		return angle
	return (angle * 180) / math.pi

def rad_to_deg(angle):
	return (angle * 180) / math.pi

def current_info():
	print("\n----------\n")
	print("Current position:")
	cur_pos = p.get_current_position()
	print(cur_pos)
	xp = cur_pos.p.x()
	yp = cur_pos.p.y()
	zp = cur_pos.p.z()
	print("\n... in other words:")
	print("x_API = "),
	print(round(xp, 6)),
	print("\t\tx_RCM = "),
	print(round(yp, 6))
	print("y_API = "),
	print(round(yp, 6)),
	print("\t\ty_RCM = "),
	print(round(xp, 6))
	print("z_API = "),
	print(round(zp, 6)),
	print("\t\tz_RCM = "),
	print(round(-zp + 0.0065, 6))
	print("\nCurrent joints position (according to API notation):")
	if radian:
		print(p.get_current_joint_position())
	else:
		j_p = p.get_current_joint_position()
		for i in range(6):	# there would be 7 joints but there are only 6 in the output. The last one is omit
			if i != 2:
				j_p[i] = rad_to_deg(j_p[i])
		print(j_p)
	print("\n----------\n")

def move_single_joint():
	n_joint = int(raw_input("Insert which joint [0 is the first, 5 is the sixth]: "))	# there would be 7 joints but there are only 6 in the output. The last one is omit
	if n_joint == 2:	# the third joint is prismatic
		value = float(raw_input("Insert absolute movement value (in meters): "))
	else:
		value = check_angle_um(float(raw_input(("Insert absolute movement value (in ") + ("rad" if radian else "deg") + "): ")))
	p.move_joint_one(value, n_joint)
	current_info()

def move_multiple_joint():
	value = []
	n_joint = []
	how_many_joints = int(raw_input("How many joints do you want to move? "))
	while how_many_joints > 6 or how_many_joints < 1:
		how_many_joints = int(raw_input("How many joints do you want to move? (There would be 7 joints but there are only 6 in the framework. The last one is omit) "))
	for i in range(how_many_joints):
		print("#" + str(i+1) + " joint to move")
		n_joint.append(int(raw_input("Insert which joint [0 is the first, 5 is the sixth]: ")))	# there would be 7 joints but there are only 6 in the output. The last one is omit
		if n_joint[len(n_joint) - 1] == 2:	# the third joint is prismatic
			value.append(float(raw_input("Insert absolute movement value (in meters): ")))
		else:
			value.append(check_angle_um(float(raw_input(("Insert absolute movement value (in ") + ("rad" if radian else "deg") + "): "))))
	p.move_joint_some(numpy.array(value), numpy.array(n_joint))
	current_info()


def inverse_kinematic():
	RCM_or_API = raw_input("Do you refer to RCM [R] / API [a] coordinates system? ")
	print ("Insert absolute position to reach (in meters):")
	x = float(raw_input("x = "))
	y = float(raw_input("y = "))
	z = float(raw_input("z = "))
	if RCM_or_API != "a":	#move from RCM to API coordinates system
		z = -z + 0.0065
		yy= x
		x = y
		y = yy
	p.move(PyKDL.Vector(x,y,z))
	current_info()

def inverse_kinematic_closed_form():
	RCM_or_API = raw_input("Do you refer to RCM [R] / API [a] coordinates system? ")
	print ("Insert absolute position to reach (in meters):")
	x = float(raw_input("x = "))
	y = float(raw_input("y = "))
	z = float(raw_input("z = "))
	if RCM_or_API == "a":	#move from API to RCM coordinates system
		z = 0.0065 - z
		yy= x
		x = y
		y = yy
	try:
		d3 = math.sqrt(x*x + y*y + z*z)
		theta1 = math.atan2(y, z)
		theta2 = math.asin(x/d3)
	except Exception as error:
		print("!!! ERROR !!! ")
		print(error)
	else:
		p.move_joint_some(numpy.array([theta1, -theta2, d3]), numpy.array([0,1,2]))
		current_info()
		print ("Joints values calculated are: ")
		print ("theta1: "),
		print (round(check_angle_um_to_deg(theta1),6)),
		print ("   (in " + ("rad" if radian else "deg") + ")")
		print ("theta2: "),
		print (round(check_angle_um_to_deg(theta2),6)),
		print ("   (in " + ("rad" if radian else "deg") + ")")
		print ("d3: "),
		print (round(d3,6)),
		print ("   (in meters)")


numpy.set_printoptions(suppress=True)

p = dvrk.psm('PSM1')

print("Going to home to obtain arm ready...")
p.home()

print("In this job are used both the dVRK [API] reference system and the reference system used by me in the document [RCM]\n")

radian = True

while 1:
	print("\nSelect the desidered function:")
	print("1. Get current position and current joints position")
	print("2. Move a single joint (forward kinematic)")
	print("3. Move multiple joints (forward kinematic)")
	print("4. Move EE to an absolute position (inverse kinematic) by PyKDL")
	print("5. Move EE to an absolute position (inverse kinematic) in closed form")
	print(("6. Change radian / degree input-output type. Now is ") + ("RADIAN" if radian else "DEGREE"))
	print("0. Exit")
	choice = int(raw_input(" > Your choice: "))




	if choice == 0:
		exit()
	elif choice == 1:
		current_info()
	elif choice == 2:
		move_single_joint()
	elif choice == 3:
		move_multiple_joint()
	elif choice == 4:
		inverse_kinematic()
	elif choice == 5:
		inverse_kinematic_closed_form()
	elif choice == 6:
		radian = not radian
		print("Set " + ("RADIAN" if radian else "DEGREE") + " correctly")




