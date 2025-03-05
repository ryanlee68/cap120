from dorna2 import Dorna
import time
import requests

# Connect to the robot
robot = Dorna()
robot.connect("169.254.81.54")  # Replace with your robot's IP address

# Function to set digital output
def set_output(pin, state):
    command = {
        'cmd': 'output',
        'out{}'.format(pin): state
    }
    robot.play(command)

# Activate the solenoid
set_output(0, 0)  # Set output 0 to logic low to turn on the solenoid
time.sleep(2)     # Keep the solenoid on for 2 seconds

# Deactivate the solenoid
set_output(0, 1)  # Set output 0 to logic high to turn off the solenoid

# Disconnect from the robot
robot.close()