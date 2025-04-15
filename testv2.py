from dorna2 import Dorna
import time
# Connect to the robot
robot = Dorna()
robot.connect("169.254.154.191")  # Replace with your robot's IP address

vel = 1900
accel = 900
jerk = 900
turn = 0
cont = 0
j5_angle = 0 # cannister motor

def e_stop():
    if robot.get_input(7) == 0: # NC, low = triggered
        robot.halt()
        print("Emergency Stop Activated, Robot Halted")
        start_time = time.time()
        while robot.get_input(7) == 0:
            time_passed = time.time() - start_time
            print(f"Robot stopped for {int(time_passed)} seconds...")
            time.sleep(1)
        if robot.get_input(7) == 1:
            print("Emergency Stop released, Resuming operation")
            # robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=177.8,j1=177.8,j2=-139.8,j3=132.9,j4=0,j5=0)

# def laser_detect():
#     if robot.get_input(5) == 1: # green light
#         time.sleep(1)
#         if robot.get_input(5) == 1:
#             robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=0,j1=0,j2=0,j3=0,j4=0) # continue to box
#     elif robot.get_input(4) == 1: # red light
#         time.sleep(1)
#         if robot.get_input(4) == 1:
#             robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=0,j1=0,j2=0,j3=0,j4=0) # go to trash
#             robot.output(0,1) # unsuck NC, high = off

# def laser_detect():
#     robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=-22.404375,j1=-24.0345,j2=-1.0015,j3=-61.03125,j4=-243.39375) # laser location
#     time.sleep(1)
#     if robot.get_input(4) == 1: # 24v high green light 
#         # robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=0,j1=0,j2=0,j3=0,j4=0)# continue to box
#         print("1 lid detected, continuing to box")
#     elif robot.get_input(5) == 1: # 24v high red light
#         print("2 lids detected, moving to reject pile")
#         robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=0,j1=0,j2=0,j3=0,j4=0) # go to trash
#         robot.output(0,1) # unsuck NC, high = off
#         # robot.output(2,0) # air knife blow lid off
#         time.sleep(1)
#         # robot.output(2,1)
            
def come_to_me():
    e_stop()
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=90.68625,j1=0,j2=0.308,j3=0,j4=175.84875,j5=0)

def reset():
    e_stop()
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j1=90)
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j2=0)
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j3=0)
        
def check_canister(): # alarm is triggered when j5 is going back to 0 after reaching threshold
    e_stop()
    joints = robot.get_all_joint()
    j5_current = joints[5]
    print("Cannister position:", j5_current)
    # print("Canniser position:", angle)
    if j5_current >= 360:
        robot.jmove(j5=0, vel=vel, accel=accel, jerk=jerk, turn=turn, cont=cont)                               
        print("Cannister almost emtpy, Please Refill")
        global j5_angle
        j5_angle = 0
        input("Please press enter when cannister has been refilled")
        time.sleep(5)
        print("Cannister has been refilled, resuming operation")
        
def slot(further, col):
    global j5_angle
    e_stop()
    # laser_detect()
    if further:
        if col == 1:
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=89.308125,j1=14.9445,j2=-35.359,j3=24.1425,j4=-42.0075, j5=j5_angle)
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = 5)

        if col == 2:
            # robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=87.609375,j1=20.1735,j2=-30.778,j3=13.08375,j4=-84.34125,j5=0)
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=89.4825,j1=18.5175,j2=-29.266,j3=12.7125,j4=-106.47, j5=j5_angle)
            # robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = 5)
        if col == 3:
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=87.103125,j1=6.966,j2=-30.9985,j3=28.845,j4=195.5925, j5=j5_angle)
            # robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = 5)
    else:
        if col == 1:
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, j4=35.94375)

            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=88.38,j2=-99.7045,j3=-113.79375,j4=35.94375, j5=j5_angle)
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j1=28.8045)
        if col == 2:

            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=86.844375)
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=86.844375,j1=39.1995)
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=86.844375,j1=39.1995,j2=-102.4145,j3=-117.48375,j4=91.06875, j5=j5_angle)
        if col == 3:
            pass

    j5_angle += 35
    check_canister()


def z_move(z = -45):
    e_stop()
    robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, z = z)

def alt_force_drop():
    e_stop()
    robot.jmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j2=5)
    robot.jmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j1=5)
    # robot.jmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=-5)
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j1=25)

def force_drop(further, row):
    e_stop()
    if further:
        if row < 16:
            current = robot.get_all_joint()
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=current[0],j1=current[1]+6,j2=current[2]-8,j3=current[3]-16,j4=current[4]-3)
        else:
            current = robot.get_all_joint()
            robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=current[0],j1=current[1]+3,j2=current[2],j3=current[3]-16,j4=current[4]-3)
    else:
        current = robot.get_all_joint()
        robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=current[0],j1=current[1]+5,j2=current[2]+5,j3=current[3]+5,j4=current[4])

def mid_can(x, y):
    e_stop()
    # robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=39.639375,j1=59.8995,j2=-24.2485,j3=-122.3775,j4=101.6325)
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=35.364375,j1=64.368,j2=-37.96,j3=-113.88375,j4=86.81625)
    robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,x=x, y=y)

def canister(zone):
    e_stop()
    # suck
    robot.output(0,0)
    if zone == 1:
        z = 55
        mid_can(4,-10)
        # mid_can(0,0)
        # robot.close()
        z_move(z=-z)
        z_move(z=z)
        # robot.jmove(rel=1,vel=25,accel=500,jerk=2500,turn=turn,cont=True,j3=5)
        # robot.jmove(rel=1,vel=25,accel=500,jerk=2500,turn=turn,cont=True,j3=-5)
        # robot.jmove(rel=1,vel=25,accel=500,jerk=2500,turn=turn,cont=True,j3=5)
        # robot.jmove(rel=1,vel=25,accel=500,jerk=2500,turn=turn,cont=True,j3=-5)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=-3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=-3)
        robot.jmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=20)
        print("lol")
    elif zone == 2:
        z = 55
        # mid_can(-10,-10)
        mid_can(5,5)
        z_move(z=-z)
        z_move(z=z)
        # robot.close()

        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=-3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=-3)
        robot.jmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=20)
    elif zone == 3:
        z = 55
        mid_can(-10,-15)
        z_move(z=-z)
        z_move(z=z)

        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=-3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=-3)
    elif zone == 4:
        mid_can(4,11)
        z_move(z=-38)
        z_move(z=38)

        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=-3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=-3)
        robot.jmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=20)
    elif zone == 5:
        z = 55
        mid_can(-5,10)
        
        z_move(z=-z)
        z_move(z=z)

        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=-3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=-3)
        robot.jmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=20)
    elif zone == 6:
        mid_can(0,-11)
        z_move(z=-38)
        z_move(z=38)

        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=-3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=3)
        robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=turn,cont=True,j3=-3)
        robot.jmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=20)
    pass
    

def dynamic_slot(row, col):
    e_stop()
    mult_dict = {
        1:12.5,
        2:12.5,
        3:12.5,
        4:16.5,
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
            # unsuck
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = y_down)
            z_move(z=-40)
            robot.output(0,1)
            # time.sleep(1)

            force_drop(further, row=row)
            z_move(z=45)
        
        if col == 2:
            zone = 3
            canister(zone=zone)
            multiple = mult_dict[zone]
            y_down = row * -multiple + multiple
            slot(further, col)
            # unsuck
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = y_down)
            z_move(z=-45)
            robot.output(0,1)
            force_drop(further, row=row)
            z_move(z=45)
        if col == 3:
            zone = 5
            canister(zone=zone)
            multiple = mult_dict[zone]
            y_down = row * -multiple + multiple
            slot(further, col)
            # unsuck
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = y_down)
            z_move(z=-45)
            robot.output(0,1)
            force_drop(further, row=row)
            z_move(z=45)
    elif row >= 21 and row <= 25:
        further = False
        if col == 1:
            zone = 2
            canister(zone=zone)
            multiple = mult_dict[zone]
            # temp_row = row - 25
            y_down = abs(row-25) * multiple
            # y_down = 30
            print(y_down)
            slot(further, col)
            # unsuck
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = y_down)
            z_move(z=-20)
            robot.output(0,1)
            # force_drop(further, row=row)
            # alt_force_drop()
            # z_move(z=45)

        if col == 2:
            zone = 4
            canister(zone=zone)
            multiple = mult_dict[zone]
            y_down = abs(row-25) * multiple
            print(y_down)
            slot(further, col)
            # unsuck
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = y_down)
            z_move(z=-25)
            robot.output(0,1)
            # force_drop(further, row=row)
            z_move(z=45)
        if col == 3:
            zone = 6
            canister(zone=zone)
            multiple = mult_dict[zone]
            y_down = row * -multiple + multiple
            slot(further, col)
            # unsuck
            robot.lmove(rel=1,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont, y = y_down)
            z_move(z=-60)
            robot.output(0,1)
            # force_drop(further, row=row)
            z_move(z=45)
    else:
        print(f"Slot with row: {row} andd column: {col} does not exist. Stopping Robot")
        robot.log(msg=f"Slot with row: {row} andd column: {col} does not exist. Stopping Robot")
        robot.close()


# robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j1=70)
# robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j2=0)
# dynamic_slot(row=2, col=1)


for j in range(1,25):
    for i in range(1,4):
        robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j1=70)
        robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j2=0)
        dynamic_slot(row=j, col=i)


robot.close()