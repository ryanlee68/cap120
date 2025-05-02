from dorna2 import Dorna
import time

# Connect to the robot
robot = Dorna()
robot.connect("169.254.81.54")


while True:
    # robot.output(4,1)
    # time.sleep(5)
    # robot.output(4,0)
    # time.sleep(5)
    print(f"robot.get_input(6): {robot.get_input(6)}")
    print(f"robot.get_input(2): {robot.get_input(2)}")
    if robot.get_input(6) == 1: # 1 lid
        print("1 LID DETECTED")
        # robot.output(4,0)
        # time.sleep(2)
        # robot.output(4,0)
        # time.sleep(2)
    elif robot.get_input(4) == 0:
        print("2+ or no LID DETECTED")
        # robot.output(4,1)
        # robot.output(4,1)
        # time.sleep(2)
        # robot.output(4,0)
        # time.sleep(2)
    print("------------------------")
    time.sleep(1)
    
