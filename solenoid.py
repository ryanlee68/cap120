from dorna2 import Dorna
import time
from .Robot import Robot
import requests

# Connect to the robot
# robot = Dorna()

# robot.connect("169.254.81.54")
vel = 1900
accel = 900
jerk = 900
turn = 0
cont = True

ip = "169.254.81.54"
dorna = Dorna()
dorna.connect(ip)

robot = Robot(dorna, vel, accel, jerk, turn, cont)

robot.startup()
while True:
    print("Waiting for input...")
    # robot.dorna.output(0,0)
    time.sleep(5)
    # robot.dorna.output(0,1)
    # time.sleep(2)
    robot.dorna.output(1,1)
    time.sleep(5)
    robot.dorna.output(1,0)
# dorna.robot.output(4,1)
# dorna.robot.output(0,1)
robot.dorna.output(0,0)
# dorna.robot.jmove(rel=0,vel=dorna.vel,accel=dorna.accel,jerk=dorna.jerk,turn=dorna.turn,cont=dorna.cont,j1=70, j2=0)
# unsuck
# robot.output(0,1)
# suck
# robot.output(4,1)
# robot.close()
# dorna.robot.jmove(rel=1,vel=dorna.vel,accel=dorna.accel,jerk=dorna.jerk,turn=dorna.turn,cont=dorna.cont,j5=-2)



# 🟢[21:16:18]{"id":236210,"stat":2}
# 🟢[21:16:18]{"id":252382,"stat":0}
# 🟢[21:16:18]{"id":856144,"stat":-1}
# 🟢[21:16:18]{"id":722584,"stat":0}
# 🟢[21:16:18]{"id":722584,"stat":1}
# 🟢[21:16:18]{"cmd":"axis","id":722584,"ratio5":1,"ratio6":20,"ratio7":20}
# 🟢[21:16:18]{"id":722584,"stat":2}
# 🟢[21:16:18]{"id":252382,"stat":1}
# 🟢[21:16:18]{"cmd":"uid","id":252382,"uid":"310024001751313232343031"}
# 🟢[21:16:18]{"id":252382,"stat":2}
# 🟢[21:16:19]{"cmd":"alarm","alarm":1,"err0":0,"err1":0,"err2":0,"err3":0,"err4":0,"err5":-744,"err6":0,"err7":0}

# 🟢[21:17:11]{"id":311345,"stat":2}
# 🟢[21:17:11]{"id":215797,"stat":-1}
# 🟢[21:17:11]{"id":705315,"stat":0}
# 🟢[21:17:11]{"id":705315,"stat":1}
# 🟢[21:17:11]{"cmd":"axis","id":705315,"ratio5":1,"ratio6":20,"ratio7":20}
# 🟢[21:17:11]{"id":705315,"stat":2}
# 🟢[21:17:11]{"id":442236,"stat":1}
# 🟢[21:17:11]{"cmd":"adc","id":442236,"adc0":29460,"adc1":42956,"adc2":37766,"adc3":37814,"adc4":37799}
# 🟢[21:17:11]{"id":442236,"stat":2}
# 🟢[21:17:11]{"id":60018,"stat":1}
# 🟢[21:17:11]{"cmd":"uid","id":60018,"uid":"310024001751313232343031"}
# 🟢[21:17:11]{"id":60018,"stat":2}

# {"cmd":"pwm","id":863583,"pwm0":0,"pwm1":0,"pwm2":0,"pwm3":0,"pwm4":0,"pwm5":0"duty0":0,"duty1":0,"duty2":0,"duty3":0,"duty4":0,"duty5":0,"freq0":0,"freq1":0,"freq2":0,"freq3":0,"freq4":0,"freq5":0}