from dorna2 import Dorna
import time
import queue
import dorna2.ws
import types

class Robot:
    vel = 1900
    accel = 900
    jerk = 900
    turn = 0
    cont = 0

    def __init__(self, ip):
        self.robot = Dorna()
        self.robot.connect(ip)  # Replace with your robot's IP address

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
        self.robot.output(0,0)
    
    def unsuck(self):
        self.robot.output(0,1)

    def load_cell(self):
        self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=35.724375,j1=15.381,j2=-59.5015,j3=-44.76375,j4=91.18125)
        self.z_move(-35)
        self.unsuck()
        time.sleep(3)
        if self.robot.get_input(6) == 1:
            print("only one seal detected")
            self.z_move(-10)
            self.suck()
            self.z_move(45)
            return True
        elif self.robot.get_input(6) == 0:
            self.trash()
            return False
    
    def trash(self):
        print("Duplicate Lid detected: Air knife activated")

    def jerk_move(self):
        jerk_amount = 3
        self.robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=self.turn,cont=True,j3=jerk_amount)
        self.robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=self.turn,cont=True,j3=-jerk_amount)
        self.robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=self.turn,cont=True,j3=jerk_amount)
        self.robot.jmove(rel=1,vel=50000,accel=50000,jerk=250000,turn=self.turn,cont=True,j3=-jerk_amount)
        # self.robot.play(file="scripts/jerk.txt")

    def linear_act(self, joint_move):
        self.robot.jmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j5=joint_move)

    def startup(self):
        self.robot.play(file="scripts/startup.txt")

    def come_to_me(self):
        self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=90.68625,j1=0,j2=0.308,j3=0,j4=175.84875)

    def reset(self):
        self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j1=90)
        self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j2=0)
        self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j3=0)


    def slot(self, further, col):
        if further:
            if col == 1:
                self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=89.308125,j1=14.9445,j2=-35.359,j3=24.1425,j4=-42.0075)
                # self.robot.lmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont, y = 5)

            if col == 2:
                self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=87.609375,j1=20.1735,j2=-30.778,j3=13.08375,j4=-84.34125)
                self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=89.4825,j1=18.5175,j2=-29.266,j3=12.7125,j4=-106.47)
                # robot.lmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont, y = 5)
            if col == 3:
                self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=87.103125,j1=6.966,j2=-30.9985,j3=28.845,j4=195.5925)
                # self.robot.lmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont, y = 5)
        else:
            if col == 1:
                self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont, j4=35.94375)

                self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=88.38,j2=-99.7045,j3=-113.79375,j4=35.94375)
                self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j1=28.8045)
            if col == 2:

                self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=86.844375)
                self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=86.844375,j1=39.1995)
                self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=86.844375,j1=39.1995,j2=-102.4145,j3=-117.48375,j4=91.06875)
            if col == 3:
                pass


    def z_move(self, z = -45):
        self.robot.lmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont, z = z)

    def alt_force_drop(self):

        self.robot.jmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j2=5)
        self.robot.jmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j1=5)
        # self.robot.jmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=-5)
        self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j1=25)

    def force_drop(self, further, row):
        if further:
            if row < 16:
                current = self.robot.get_all_joint()
                self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=current[0],j1=current[1]+6,j2=current[2]-8,j3=current[3]-16,j4=current[4]-3)
            else:
                current = self.robot.get_all_joint()
                self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=current[0],j1=current[1]+3,j2=current[2],j3=current[3]-16,j4=current[4]-3)
        else:
            current = self.robot.get_all_joint()
            self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=current[0],j1=current[1]+5,j2=current[2]+5,j3=current[3]+5,j4=current[4])

    def mid_can(self, x, y):
        self.robot.jmove(rel=0,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=-0.084375,j1=79.281,j2=-63.718,j3=-102.58875,j4=90.97875)
        self.robot.lmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,x=x, y=y)

    def canister(self, zone):
        # suck
        self.suck()
        if zone == 1:
            z = 50
            # self.mid_can(4,-10)
            self.mid_can(0,0)
            self.z_move(z=-z)
            self.z_move(z=z)
            self.jerk_move()
            self.robot.jmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=45)
        elif zone == 2:
            z = 50
            # self.mid_can(5,5)
            self.mid_can(0,0)
            self.z_move(z=-z)
            self.z_move(z=z)
            self.jerk_move()
            self.robot.jmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=45)
        elif zone == 3:
            z = 45
            # self.mid_can(-10,-15)
            self.mid_can(0,0)
            self.z_move(z=-z)
            self.z_move(z=z)
            self.jerk_move()
            self.robot.jmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=45)
        elif zone == 4:
            # self.mid_can(4,11)
            self.mid_can(0,0)
            self.z_move(z=-45)
            self.z_move(z=45)
            self.jerk_move()
            self.robot.jmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=45)
        elif zone == 5:
            z = 45
            # self.mid_can(-5,10)
            self.mid_can(0,0)
            
            self.z_move(z=-z)
            self.z_move(z=z)
            self.jerk_move()
            self.robot.jmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=45)
        elif zone == 6:
            # self.mid_can(0,-11)
            self.mid_can(0,0)
            self.z_move(z=-38)
            self.z_move(z=38)
            self.jerk_move()
            self.robot.jmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont,j0=45)
        pass


    def dynamic_slot(self, row, col):
        mult_dict = {
            1:12.5,
            2:12.5,
            3:12.5,
            4:16.5,
            5:12.5,
            6:12.5
        }
        if row < 19:
            further = True
            if col == 1:
                zone = 1
                self.canister(zone=zone)
                multiple = mult_dict[zone]
                y_down = row * -multiple + multiple
                if not self.load_cell():
                    return False

                self.slot(further, col)
                # unsuck
                self.robot.lmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont, y = y_down)
                self.z_move(z=-40)
                self.unsuck()
                # time.sleep(1)

                self.force_drop(further, row=row)
                self.z_move(z=45)
            
            if col == 2:
                zone = 3
                self.canister(zone=zone)
                multiple = mult_dict[zone]
                y_down = row * -multiple + multiple
                self.slot(further, col)
                # unsuck
                self.robot.lmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont, y = y_down)
                self.z_move(z=-45)
                self.unsuck()
                self.force_drop(further, row=row)
                self.z_move(z=45)
            if col == 3:
                zone = 5
                self.canister(zone=zone)
                multiple = mult_dict[zone]
                y_down = row * -multiple + multiple
                self.slot(further, col)
                # unsuck
                self.robot.lmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont, y = y_down)
                self.z_move(z=-45)
                self.unsuck()
                self.force_drop(further, row=row)
                self.z_move(z=45)
        elif row >= 21 and row <= 25:
            further = False
            if col == 1:
                zone = 2
                self.canister(zone=zone)
                multiple = mult_dict[zone]
                # temp_row = row - 25
                y_down = abs(row-25) * multiple
                # y_down = 30
                print(y_down)
                self.slot(further, col)
                # unsuck
                self.robot.lmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont, y = y_down)
                self.z_move(z=-20)
                self.unsuck()
                # force_drop(further, row=row)
                # alt_force_drop()
                # z_move(z=45)

            if col == 2:
                zone = 4
                self.canister(zone=zone)
                multiple = mult_dict[zone]
                y_down = abs(row-25) * multiple
                print(y_down)
                self.slot(further, col)
                # unsuck
                self.robot.lmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont, y = y_down)
                self.z_move(z=-25)
                self.unsuck()
                # force_drop(further, row=row)
                self.z_move(z=45)
            if col == 3:
                zone = 6
                self.canister(zone=zone)
                multiple = mult_dict[zone]
                y_down = row * -multiple + multiple
                self.slot(further, col)
                # unsuck
                self.robot.lmove(rel=1,vel=self.vel,accel=self.accel,jerk=self.jerk,turn=self.turn,cont=self.cont, y = y_down)
                self.z_move(z=-60)
                self.unsuck()
                # force_drop(further, row=row)
                self.z_move(z=45)
        else:
            print(f"Slot with row: {row} andd column: {col} does not exist. Stopping self.robot")
            self.robot.log(msg=f"Slot with row: {row} andd column: {col} does not exist. Stopping self.robot")
            self.robot.close()