from dorna2 import Dorna
import time
# Connect to the robot
robot = Dorna()
robot.connect("169.254.154.191")

# e stop test
while True:
    if robot.get_input(7) == 0:
        print("e stop activated")
    elif robot.get_input(7) == 1:
        print("e stop not activated")
    time.sleep(1) 
