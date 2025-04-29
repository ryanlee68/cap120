from dorna2 import Dorna
import time

# Connect to the robot
robot = Dorna()
robot.connect("169.254.154.191")


while True:
    # robot.output(4,1)
    # time.sleep(5)
    # robot.output(4,0)
    # time.sleep(5)
    if robot.get_input(6) == 0: # 1 lid
        print("1 LID DETECTED")
        robot.output(4,0)
        # time.sleep(2)
        # robot.output(4,0)
        # time.sleep(2)
    elif robot.get_input(6) == 1:
        print("2+ LID DETECTED")
        robot.output(4,1)
        # robot.output(4,1)
        # time.sleep(2)
        # robot.output(4,0)
        # time.sleep(2)
    print("------------------------")
    time.sleep(1)
    
