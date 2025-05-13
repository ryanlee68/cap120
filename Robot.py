from dorna2 import Dorna
import time
import queue
import dorna2.ws
import types
import utils

class Robot:
    # to git pull: git pull ryanlee@Ryans-MacBook-Air.local:~/Public/dorna_lab
    # scp -r ryanlee@Ryans-MacBook-Air.local:/Users/ryanlee/Public/dorna_lab /home/dorna/Downloads
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
            1:12.5,
            2:11.5,
            3:12,
            4:13,
            5:12,
            6:12
    }
    hexa_down = {
        1:-39,
        2:-65,
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
                (self.dorna.jmove, dict(j0=89.46,j1=8.4105,j2=-25.7695,j3=21.0825,j4=-42.0075)),
            ],
            2: [
                # (self.dorna.jmove, dict(j0=87.609375, j1=20.1735, j2=-30.778, j3=13.08375, j4=-84.34125)),
                (self.dorna.jmove, dict(j0=89.4825,   j1=18.5175, j2=-29.266, j3=12.7125, j4=-106.47)),
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
        self.dorna.output(0,0)
    
    def unsuck(self):
        self.dorna.output(0,1)

    def load_cell(self):
        return "1_SEAL"
        self.dorna.jmove(**self.no_rel,j0=39.47625,j1=16.488,j2=-52.522,j3=-50.805,j4=91.1025)
        # self.dorna.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=39.898125,j1=25.128,j2=-58.237,j3=-53.73,j4=91.1025)
        # self.dorna.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=35.724375,j1=15.381,j2=-59.5015,j3=-44.76375,j4=91.18125)
        self.z_move(-10)
        self.unsuck()
        self.z_move(45)
        if self.dorna.get_input(6) == 1:
            print("1 SEAL DETECTED")
            # self.dorna.output(2,1)
            # self.dorna.output(4,0)
            self.z_move(-47)
            # self.z_move(-13)
            # self.z_move(-55)
            self.suck()
            self.z_move(30)
            return "1_SEAL"
        elif self.dorna.get_input(2) == 1:
            print("2+ seal(s) detected, blowing lid off load cell")
            self.dorna.output(4,0)
            # self.dorna.output(2,0)
            while True:
                if self.dorna.get_input(6) == 0 and self.dorna.get_input(2) == 0:
                    self.dorna.output(4,1)
                    # self.dorna.output(2,0)
                    return "2_SEAL"
            # self.trash()
        elif self.dorna.get_input(2) == 0 and self.dorna.get_input(6) == 0:
            linear_num = -4
            print(f"NO SEAL detected, raising linear actuator by {linear_num}")
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


    def slot(self, zone):
        for method, params in self.zone_actions.get(zone, ()):
            method(**self.no_rel, **params)


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
        self.dorna.jmove(**self.no_rel,j0=1.513125,j1=69.318,j2=-32.29,j3=-127.83375,j4=94.24125)
        self.dorna.lmove(**self.rel,x=x, y=y)

    def canister(self):
        # suck
        self.suck()
        z = 82
        # self.mid_can(4,-10)
        self.mid_can(0,0)
        self.z_move(z=-z)
        self.z_move(z=z-30)
        self.jerk_move()
        self.z_move(z=30)
        self.dorna.jmove(**self.rel,j0=45)
        

    def hexa(self, zone:int, row:int) -> bool:
        print(f"{zone}  {row}")
        self.canister()
        multiple = self.mult_dict[zone]
        if zone < 4:
            y_down = row * -multiple + multiple
        else:
            y_down = abs(row-25) * multiple
        seal_count = self.load_cell()
        if seal_count == "2_SEAL" or seal_count == "0_SEAL":
            return False
        self.slot(zone)
        self.dorna.lmove(**self.rel, y = y_down)
        self.z_move(z=self.hexa_down[zone])
        self.unsuck()
        self.force_drop(zone)
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