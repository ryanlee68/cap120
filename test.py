from dorna2 import Dorna
import time
# Connect to the robot
robot = Dorna()
robot.connect("169.254.81.54")  # Replace with your robot's IP address

vel = 800
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


def slot(further, col):
    if further:
        if col == 1:
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=89.308125,j1=14.9445,j2=-35.359,j3=24.1425,j4=-42.0075,j5=0)
        if col == 2:
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=87.609375,j1=20.1735,j2=-30.778,j3=13.08375,j4=-84.34125,j5=0)
        if col == 3:
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=87.103125,j1=6.966,j2=-30.9985,j3=28.845,j4=195.5925,j5=0)
    else:
        if col == 1:
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=84.92625,j1=10.899,j2=-60.469,j3=-129.99375,j4=6.76125)
        if col == 2:
            pass
        if col == 3:
            pass


def z_move(z = -45):
    robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, z = z)

def force_drop(further, row):
    if further:
        if row < 16:
            current = robot.get_all_joint()
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=current[0],j1=current[1]+6,j2=current[2]-8,j3=current[3]-16,j4=current[4]-3)
        else:
            current = robot.get_all_joint()
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=current[0],j1=current[1]+3,j2=current[2],j3=current[3]-16,j4=current[4]-3)
    else:
        # put jmove that breaks the closer lids apart
        pass

def mid_can(x, y):
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=39.639375,j1=59.8995,j2=-24.2485,j3=-122.3775,j4=101.6325)
    robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,x=x, y=y)

def canister(zone):
    if zone == 1:
        z = 48
        mid_can(5,-17)
        z_move(z=-z)
        z_move(z=z)
    elif zone == 2:
        z = 65
        mid_can(0,-11)
        z_move(z=-z)
        z_move(z=z)
    elif zone == 3:
        z = 45
        mid_can(-10,-15)
        z_move(z=-z)
        z_move(z=z)
    elif zone == 4:
        mid_can(0,-11)
        z_move(z=-38)
        z_move(z=38)
    elif zone == 5:
        z = 40
        mid_can(-5,10)
        
        z_move(z=-z)
        z_move(z=z)
        robot.jmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=20)
    elif zone == 6:
        mid_can(0,-11)
        z_move(z=-38)
        z_move(z=38)



def dynamic_slot(row, col):
    mult_dict = {
        1:12.4,
        2:12.5,
        3:12.5,
        4:12.5,
        5:12.5,
        6:12.5
    }
    if row < 19:
        further = True
        if col == 1:
            zone = 1
            canister(zone=zone)
            multiple = mult_dict[zone]
            y_down = row * -multiple + multiple
            slot(further, col)
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = y_down)
            z_move(z=-30)
            force_drop(further, row=row)
            z_move(z=45)
        
        if col == 2:
            zone = 3
            canister(zone=zone)
            multiple = mult_dict[zone]
            y_down = row * -multiple + multiple
            slot(further, col)
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = y_down)
            z_move(z=-50)
            force_drop(further, row=row)
            z_move(z=45)
        if col == 3:
            zone = 5
            canister(zone=zone)
            multiple = mult_dict[zone]
            y_down = row * -multiple + multiple
            slot(further, col)
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = y_down)
            z_move(z=-45)
            force_drop(further, row=row)
            z_move(z=45)
    elif row >= 19 and row <= 25:
        further = False
        if col == 1:
            zone = 2
            canister(zone=zone)
            multiple = mult_dict[zone]
            y_down = row * -multiple + multiple
            slot(further, col)
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = y_down)
            z_move(z=-60)
            force_drop(further, row=row)
            z_move(z=45)
        if col == 2:
            zone = 4
            canister(zone=zone)
            multiple = mult_dict[zone]
            y_down = row * -multiple + multiple
            slot(further, col)
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = y_down)
            z_move(z=-60)
            force_drop(further, row=row)
            z_move(z=45)
        if col == 3:
            zone = 6
            canister(zone=zone)
            multiple = mult_dict[zone]
            y_down = row * -multiple + multiple
            slot(further, col)
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = y_down)
            z_move(z=-60)
            force_drop(further, row=row)
            z_move(z=45)
    else:
        print(f"Slot with row: {row} andd column: {col} does not exist. Stopping Robot")
        robot.log(msg=f"Slot with row: {row} andd column: {col} does not exist. Stopping Robot")
        robot.close()



robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j1=70)
robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j2=0)
dynamic_slot(row=18, col=1)


robot.close()