from dorna2 import Dorna
import time
# Connect to the robot
robot = Dorna()
robot.connect("169.254.81.54")  # Replace with your robot's IP address

vel = 600
accel = 400
jerk = 400
turn = 0
cont = 0

def come_to_me():
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=90.68625,j1=0,j2=0.308,j3=0,j4=175.84875)

def reset():
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j1=90)
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j2=0)
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j3=0)




def further_slot():
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=88.515,j1=11.952,j2=-41.7355,j3=35.5275,j4=-34.695)

def closer_slot():
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=90.10125,j1=37.44,j2=-91.7125,j3=-123.705,j4=37.4625)
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=89.1225,j1=23.1795,j2=-68.488,j3=-130.0725,j4=31.095)

def z_move(z = -45):
    robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, z = z)

def force_drop():
    current = robot.get_all_joint()
    print(current)
    # robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=89.229375,j1=11.223,j2=-48.931,j3=28.51875,j4=-31.73625)
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=current[0],j1=current[1]+4,j2=current[2]-1,j3=current[3]-16,j4=current[4]-3)

def canister(zone):
    if zone == 1:
        robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=42.525,j1=45.1935,j2=-58.1155,j3=-72.52875,j4=91.29375)
        z_move(z=-35)
        robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=42.525,j1=45.1935,j2=-58.1155,j3=-72.52875,j4=91.29375)



def dynamic_slot(row, col):
    multiple = 12
    if row < 20:
        if col == 1:
            canister(zone=1)
            y_down = row * -multiple + multiple
            further_slot()
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = y_down)
            z_move(z=-25)
            force_drop()
            # z_move(z=45)

dynamic_slot(row=1, col=1)


robot.close()