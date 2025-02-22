from dorna2 import Dorna
import time
# Connect to the robot
robot = Dorna()
robot.connect("169.254.81.54")  # Replace with your robot's IP address

reset_script_path = "scripts/reset.txt"
canister_script_path = "scripts/canister.txt"
camera_script_path = "scripts/camera.txt"
slot_script_path = "scripts/slot.txt"


robot.play_script(file=reset_script_path)
for i in range(10):
    robot.play_script(file=canister_script_path)
    robot.play_script(file=camera_script_path)
    robot.play_script(file=slot_script_path)
robot.play_script(file=reset_script_path)

robot.close()

# {"cmd":"jmove","rel":0,"j0":178.082,"j1":180,"j2":-141.982,"j3":134.314,"j4":364.219}
# {"cmd":"jmove","rel":0,"j0":46.429,"j1":28.777,"j2":-18.682,"j3":-97.875,"j4":447.12}
# {"cmd":"jmove","rel":0,"j0":-3.133,"j1":-0.373,"j2":-34.504,"j3":37.339,"j4":356.816}
# {"cmd":"jmove","rel":0,"j0":87.396,"j1":17.986,"j2":-67.624,"j3":54.833,"j4":329.467}
# {"cmd":"jmove","rel":0,"j0":46.43,"j1":28.78,"j2":-18.68,"j3":-97.88,"j4":447.12}