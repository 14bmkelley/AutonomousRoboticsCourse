
import time

from lib import ControlThread, ControlSystem

@ControlThread
def imu_sensor():
    
    import math
    from Adafruit_BNO055.BNO055 import BNO055 as Bno
    bno = Bno(serial_port='/dev/ttyUSB0')
    if not bno.begin():
        raise RuntimeError('BNO sensor not connected')
    
    while True:
        h, r, p = bno.read_euler()
        x, y, z = bno.read_linear_acceleration()
        lin_acc = math.sqrt((x**2) + (y**2) + (z**2))
        ControlSystem().post(imu_lin_acc=lin_acc, imu_heading=h)

@ControlThread
def imu_print(imu_lin_acc, imu_heading):
    
    while True:
        ControlSystem().console.log('lin_acc: {0}, imu_heading: {1}'.format(imu_lin_acc.value, imu_heading.value))
        time.sleep(0.3)



ControlSystem().openConsole()
