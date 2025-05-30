from dorna2 import Dorna
import time
import queue
import dorna2.ws
import types
from . import utils

class Robot:
    no_air = False
    # to git pull: git pull ryanlee@Ryans-MacBook-Air.local:~/Public/dorna_lab

    # scp -r ryanlee@Ryans-MacBook-Air.local:/Users/ryanlee/Public/dorna_lab /home/dorna/Downloads
    # to update dorna package go into folder where setup.py and run:  pip install --upgrade --editable .
    # to connect to ai rasp pi: ssh cap120@10.33.62.132kl mgsf
    # pass: ingomar123!

    # scp -r /home/cap120/yolo ryanlee@Ryans-MacBook-Air.local:/Users/ryanlee/Public

    # zone 1: row 1-18 col 1
    # zone 4: row 19-25 col 1
    # zone 2: row 1-18 col 2
    # zone 5: row 19-25 col 2
    # 
    linear_act_raise_num = -5
    max_retries = 5
    threshold = {
        1:18,
        2:18,
        3:18
    }
    mult_dict = {
            1:17,
            2:16,
            3:16,
            4:13,
            5:12,
            6:12
    }
    hexa_down = {
        1:-50,
        2:-46,
        3:-50,
        4:-46,
        5:-50,
        6:-50
    }
    def __init__(self, dorna: Dorna, vel, accel, jerk, turn, cont):
        self.dorna = dorna
        # self.dorna.connect(ip)  # Replace with your robot's IP address
        self.rel = dict(
            rel=1,
            vel=vel,
            accel=accel,
            jerk=jerk,
            turn=turn,
            cont=cont,
        )
        self.no_rel = dict(
            rel=0,
            vel=vel,
            accel=accel,
            jerk=jerk,
            turn=turn,
            cont=cont,
        )
        self.zone_actions = {
            1: [
                # {"cmd":"jmove","rel":0,"j0":88.779375,"j1":8.8155,"j2":-24.6625,"j3":14.985,"j4":-45}
                (self.dorna.jmove, dict(j0=88.779375,j1=8.8155,j2=-24.6625,j3=14.985,j4=-45)),
            ],
            2: [
                # {"cmd":"jmove","rel":0,"j0":88.610625,"j1":12.8745,"j2":-21.3775,"j3":5.77125,"j4":259.57125}
                (self.dorna.jmove, dict(j0=88.610625,   j1=12.8745, j2=-21.3775, j3=5.77125, j4=259.57125)),
            ],
            3: [
                (self.dorna.jmove, dict(j0=87.103125, j1=6.966,   j2=-30.9985, j3=28.845, j4=195.5925)),
            ],
            4: [
                # j1=39.897,j2=-105.0865,j3=-114.51375,j4=35.94375
                (self.dorna.jmove, dict(j0=88.38, j2=-105.0865,j3=-114.51375, j4=35.94375)),
                (self.dorna.jmove, dict(j1=39.897)),
            ],
            5: [
                (self.dorna.jmove, dict(j0=86.844375)),
                (self.dorna.jmove, dict(j0=86.844375, j1=39.1995)),
                (self.dorna.jmove, dict(j0=86.844375, j1=39.1995, j2=-102.4145, j3=-117.48375, j4=91.06875)),
            ],
            6: [
                # no moves
            ],
        }
        self.force_drop_actions = {
            1: [
                (self.dorna.jmove, dict(j1=6,j2=-4,j3=-16,j4=-3)),
            ],
            2: [
                # (self.dorna.jmove, dict(j1=6,j2=-8,j3=-16,j4=-3)),
                (self.dorna.jmove, dict(j3=-16)),
            ],
            3: [
                (self.dorna.jmove, dict(j1=6,j2=-8,j3=-16,j4=-3)),
            ],
            4: [
                (self.dorna.jmove, dict(j1=9,j2=4,j3=15,j4=-3)),
            ],
            5: [
                (self.dorna.jmove, dict(j1=6,j2=-8,j3=-16,j4=-3)),
            ],
            6: [
                (self.dorna.jmove, dict(j1=6,j2=-8,j3=-16,j4=-3)),
            ],
        }

    def _ws_getstate(self):
        """Return a dict that *can* be pickled (drop locks, loops, sockets…)."""
        state = self.__dict__.copy()
        for k in ("msg", "loop", "reader", "writer",
                "server_thread", "callback", "_event_list"):
            state.pop(k, None)                # runtime‑only things – discard
        return state

    def _ws_setstate(self, state):
        """Re‑create the runtime objects that were skipped in __getstate__."""
        self.__dict__.update(state)
        # rebuild the runtime helpers with a safe default
        self.msg            = queue.Queue(100)
        self.loop           = None
        self.reader         = None
        self.writer         = None
        self.server_thread  = None
        self.callback       = None
        self._event_list    = []

    # Monkey‑patch the mix‑in class once, for the whole program
    dorna2.ws.WS.__getstate__ = _ws_getstate
    dorna2.ws.WS.__setstate__ = _ws_setstate

    def suck(self):
        self.dorna.output(1,0)
    
    def unsuck(self):
        self.dorna.output(1,1)

    def load_cell(self):
        # {"cmd":"jmove","rel":0,"j0":41.979375,"j1":24.1065,"j2":-60.775,"j3":-50.16375,"j4":108.30375}
        # return "1_SEAL"
        self.dorna.jmove(**self.no_rel,j0=41.979375,j1=24.1065,j2=-60.775,j3=-50.16375,j4=108.30375)
        # self.dorna.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=39.898125,j1=25.128,j2=-58.237,j3=-53.73,j4=91.1025)
        # self.dorna.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=35.724375,j1=15.381,j2=-59.5015,j3=-44.76375,j4=91.18125)
        self.unsuck()
        self.z_move(-20)
        self.z_move(45)
        # print(self.dorna.get_input(6))
        # print(self.dorna.get_input(2))
        if self.dorna.get_input(6) == 1:
            print("1 SEAL DETECTED")
            print("ttestsedf")
            # self.dorna.output(2,1)
            # self.dorna.output(4,0)
            self.z_move(-56)
            # self.z_move(-13)
            # self.z_move(-55)
            self.suck()
            self.z_move(50)
            return "1_SEAL"
        elif self.dorna.get_input(2) == 1:
            print("2+ seal(s) detected, blowing lid off load cell")
            self.dorna.output(3,0)
            # self.dorna.output(2,0)
            while True:
                if self.dorna.get_input(6) == 0 and self.dorna.get_input(2) == 0:
                    self.dorna.output(3,1)
                    # self.dorna.output(2,0)
                    return "2_SEAL"
            # self.trash()
        elif self.dorna.get_input(2) == 0 and self.dorna.get_input(6) == 0:
            linear_num = -4
            print(f"NO SEAL detected, raising linear actuator by {linear_num}")
            if self.no_air:
                pass
            else:
                self.linear_act(linear_num)
            return "0_SEAL"

    def jerk_move(self):
        jerk_amount = 5
        self.dorna.jmove(rel=1,vel=50000,accel=50000,jerk=250000,cont=True,j3=jerk_amount)
        self.dorna.jmove(rel=1,vel=50000,accel=50000,jerk=250000,cont=True,j3=-jerk_amount)
        self.dorna.jmove(rel=1,vel=50000,accel=50000,jerk=250000,cont=True,j3=jerk_amount)
        self.dorna.jmove(rel=1,vel=50000,accel=50000,jerk=250000,cont=True,j3=-jerk_amount)
        self.dorna.jmove(rel=1,vel=50000,accel=50000,jerk=250000,cont=True,j3=jerk_amount)
        self.dorna.jmove(rel=1,vel=50000,accel=50000,jerk=250000,cont=True,j3=-jerk_amount)
        time.sleep(0.5)
        

    def linear_act(self, joint_move=linear_act_raise_num):
        self.dorna.jmove(**self.rel,j5=joint_move)

    def startup(self):
        self.dorna.play(file="scripts/startup.txt")

    def come_to_me(self):
        self.dorna.jmove(**self.no_rel,j0=90.68625,j1=0,j2=0.308,j3=0,j4=175.84875)

    def reset(self):
        self.dorna.jmove(**self.no_rel,j1=90)
        self.dorna.jmove(**self.no_rel,j2=0)
        self.dorna.jmove(**self.no_rel,j3=0)


        


    def z_move(self, z = -45):
        self.dorna.lmove(**self.rel, z = z)

    def alt_force_drop(self):
        self.dorna.jmove(**self.rel, j2=5)
        self.dorna.jmove(**self.rel, j1=5)
        self.dorna.jmove(**self.no_rel, j1=25)

    def force_drop(self, zone):
        for method, params in self.force_drop_actions.get(zone, ()):
            method(**self.rel, **params)
        

    def mid_can(self, x, y):
        
        # {"cmd":"jmove","rel":0,"j0":1.119375,"j1":73.6875,"j2":-41.065,"j3":-119.1375,"j4":91.5075}

        self.dorna.jmove(**self.no_rel,j0=1.119375,j1=73.6875,j2=-41.065,j3=-119.1375,j4=91.5075)


        self.dorna.lmove(**self.rel,x=x, y=y)

    def canister(self):
        
        # suck
        self.suck()
        z = 83
        # self.mid_can(4,-10)
        self.mid_can(0,0)
        self.z_move(z=-z)
        self.z_move(z=z-30)
        self.jerk_move()
        self.z_move(z=30)
        self.dorna.jmove(**self.rel,j0=45)
        
    def slot(self, zone, row):
        multiple = self.mult_dict[zone]
        last_slot = utils.get_last_slot(zone)
        if last_slot[1] == (zone, row-1):
            self.dorna.jmove(**self.no_rel,
                             j0=last_slot[0][0], 
                             j1=last_slot[0][1], 
                             j2=last_slot[0][2], 
                             j3=last_slot[0][3], 
                             j4=last_slot[0][4],
                            )
            if zone < 4:
                y_down = -multiple
            else:
                y_down = -multiple
        else:
            if zone < 4:
                y_down = row * -multiple + multiple
            else:
                y_down = abs(row-25) * multiple
            for method, params in self.zone_actions.get(zone, ()):
                method(**self.no_rel, **params)
        print(f"y_down: {y_down}")
        self.dorna.lmove(**self.rel, y = y_down)
        return ((self.dorna.get_all_joint(), (zone, row)))

    def hexa(self, zone:int, row:int) -> bool:
        print(f"{zone}  {row}")
        self.canister()
        seal_count = self.load_cell()
        if seal_count == "2_SEAL" or seal_count == "0_SEAL":
            return False
        last_slot = self.slot(zone, row)
        print(f"Last slot: {last_slot}")
        # self.z_move(z=self.hexa_down[zone])
        self.z_move(z=self.hexa_down[zone])
        self.unsuck()
        self.force_drop(zone)
        utils.save_last_slot(last_slot)
        self.z_move(z=55)
        return True


    def dynamic_slot(self, row, col):
        for attempt in range(self.max_retries):
            if attempt>0:
                utils.count()
                print(f"Count: {utils.get_count()}")
                if utils.check_count():
                    print(f"Linear Actuator has been raised at count: {utils.get_count()}")
                    self.linear_act()

            self.dorna.jmove(**self.no_rel,j1=70, j2=0)
            if row <= self.threshold[1]:
                further = True
                if col == 1:
                    zone = 1
                    if self.hexa(zone, row):
                        return True
                    else:
                        print(f"Retry {attempt+1}/{self.max_retries} …")
                        continue
                
                if col == 2:
                    zone = 2
                    if self.hexa(zone, row):
                        return True
                    else:
                        print(f"Retry {attempt+1}/{self.max_retries} …")
                        continue
                if col == 3:
                    zone = 3
                    if self.hexa(zone, row):
                        return True
                    else:
                        print(f"Retry {attempt+1}/{self.max_retries} …")
                        continue
            elif row > self.threshold[1] and row <= 25:
                further = False
                if col == 1:
                    zone = 4
                    if self.hexa(zone, row):
                        return True
                    else:
                        print(f"Retry {attempt+1}/{self.max_retries} …")
                        continue

                if col == 2:
                    zone = 4
                    zone = 2
                    if self.hexa(zone, row):
                        return True
                    else:
                        print(f"Retry {attempt+1}/{self.max_retries} …")
                        continue
                if col == 3:
                    zone = 6
                    zone = 2
                    if self.hexa(zone, row):
                        return True
                    else:
                        print(f"Retry {attempt+1}/{self.max_retries} …")
                        continue
            else:
                print(f"Slot with row: {row} andd column: {col} does not exist. Stopping self.dorna")
                self.dorna.log(msg=f"Slot with row: {row} andd column: {col} does not exist. Stopping self.dorna")
                self.dorna.close()
        return False