from dorna2 import Dorna
import time
# Connect to the robot
robot = Dorna()
robot.connect("169.254.81.54")  # Replace with your robot's IP address

vel = 200
accel = 100
jerk = 100
turn = 0
cont = 0


def reset():
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j1=90)
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j2=0)
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j3=0)


def canister():
    # robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=46.429, j1=28.777,j2 = -18.682,j3=-97.875,j4=447.12)
    # robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=45.646875, j1=16.5555,j2 = -7.4545,j3=-97.70625,j4=447.08625)

    # robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=53.37, j1=14.346,j2 = -6.6085,j3=-96.04125,j4=483.10875)
    # robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=52.531875, j1=26.3115,j2 = -28.6045,j3=-94.39875,j4=461.66)
    # {"cmd":"jmove","rel":0,"j0":52.531875,"j1":26.3115,"j2":-28.6045,"j3":-94.39875,"j4":461.66}
    # {"cmd":"jmove","rel":0,"j0":49.123125,"j1":11.088,"j2":3.8225,"j3":-107.49375,"j4":815.81625}

    # robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=46.429, j1=28.777,j2 = -18.682,j3=-97.875,j4=447.12)
    robot.play_script(file="scripts/test.txt")

def slot():
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=91.749375, j1=27.828,j2 = -38.176,j3=14.81625,j4=661.42125)
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=92.311875, j1=4.284,j2 = -24.1585,j3=19.63125,j4=659.86875)
#     {"cmd":"jmove","rel":0,"j0":91.873125,"j1":13.239,"j2":-43.162,"j3":24.89625,"j4":665.11125}
# {"cmd":"jmove","rel":0,"j0":91.231875,"j1":20.2455,"j2":-55.429,"j3":29.7225,"j4":666.495}
    # {"cmd":"jmove","rel":0,"j0":93.661875,"j1":21.3525,"j2":-57.3685,"j3":32.07375,"j4":654.35625}
    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=93.661875, j1=21.3525,j2 = -57.3685,j3=32.07375,j4=654.35625)

    robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j0=91.749375, j1=27.828,j2 = -38.176,j3=14.81625,j4=661.42125)



reset()
canister()
slot()
# for i in range(10):
    # robot.play_script(file=canister_script_path)
    # robot.play_script(file=camera_script_path)
    # robot.play_script(file=slot_script_path)


# test_script_path = "scripts/test.txt"
# robot.play_script(file=test_script_path)

# robot.play_script(file=reset_script_path)

robot.close()

# {"cmd":"jmove","rel":0,"j0":178.082,"j1":180,"j2":-141.982,"j3":134.314,"j4":364.219}
# {"cmd":"jmove","rel":0,"j0":46.429,"j1":28.777,"j2":-18.682,"j3":-97.875,"j4":447.12}
# {"cmd":"jmove","rel":0,"j0":-3.133,"j1":-0.373,"j2":-34.504,"j3":37.339,"j4":356.816}
# {"cmd":"jmove","rel":0,"j0":87.396,"j1":17.986,"j2":-67.624,"j3":54.833,"j4":329.467}
# {"cmd":"jmove","rel":0,"j0":46.43,"j1":28.78,"j2":-18.68,"j3":-97.88,"j4":447.12}