from dorna2 import Dorna

# Connect to the robot
robot = Dorna()
robot.connect("169.254.81.54")  # Replace with your robot's IP address

# # Enter calibration mode
vel1 = 75
acc1 = 1
robot.jmove(timeout=-1, rel=0, vel=vel1 ,j0=0)
robot.jmove(timeout=-1, rel=0, vel=vel1,j1=0)
robot.jmove(timeout=-1, rel=0, vel=vel1,j2=0)
robot.jmove(timeout=-1, rel=0, vel=vel1,j3=0)
robot.jmove(timeout=-1, rel=0, vel=vel1 ,j4=0)

# back to set joints
robot.jmove(timeout=1, rel=0, vel=vel1, acc=acc1 ,j0=180)
robot.jmove(timeout=0, rel=0, vel=vel1, acc=acc1 ,j1=120)
robot.jmove(timeout=0, rel=0, vel=vel1, acc=acc1 ,j2=-142)
robot.jmove(timeout=0, rel=0, vel=vel1, acc=acc1 ,j3=135)
robot.jmove(timeout=-1, rel=0, vel=vel1, acc=acc1 ,j4=0)
robot.jmove(timeout=0, rel=0, vel=vel1, acc=acc1 ,j1=180)
robot.close()