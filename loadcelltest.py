from dorna2 import Dorna
import time

# Connect to the robot
robot = Dorna()
robot.connect("169.254.154.191")


while True:
    if robot.get_input(6) == 1:
        print("1 LID DETECTED")
    elif robot.get_input(6) == 0:
        print("2+ LID DETECTED")
    print("------------------------")
    time.sleep(1)
    
