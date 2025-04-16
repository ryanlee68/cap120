from Robot import Robot
from dorna2 import Dorna
import time
# Connect to the robot

ip = "169.254.81.54"
dorna = Robot(ip)

dorna.startup()
dorna.robot.jmove(rel=0,vel=dorna.vel,accel=dorna.accel,jerk=dorna.jerk,turn=dorna.turn,cont=dorna.cont,j1=70, j2=0)
dorna.dynamic_slot(row=1, col=1)
dorna.linear_act(1)


# for j in range(1,25):
#     for i in range(1,4):
#         robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j1=70)
#         robot.jmove(rel=0,vel=vel,accel=accel,jerk=jerk,turn=turn,cont=cont,j2=0)
#         dynamic_slot(row=j, col=i)


dorna.robot.close()
