from dorna2 import Dorna
import time

# Connect to the robot
robot = Dorna()
robot.connect("169.254.154.191")


while True:
    if robot.get_input(4) == 1:
        print("GREEN ON")
    elif robot.get_input(4) == 0:
        print("GREEN OFF")
    if robot.get_input(5) == 1:
        print("RED ON")
    elif robot.get_input(5) == 0:
        print("RED OFF")
    print("------------------------")
    time.sleep(1)
    
