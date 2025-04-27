from dorna2 import Dorna
import time

# Connect to the robot
robot = Dorna()
robot.connect("169.254.81.54")


while True:
    if robot.get_input(6) == 0:
        print("1 or 0 LID DETECTED")
    elif robot.get_input(6) == 1:
        print("2+ LID DETECTED")
    print("------------------------")
    time.sleep(1)
    
