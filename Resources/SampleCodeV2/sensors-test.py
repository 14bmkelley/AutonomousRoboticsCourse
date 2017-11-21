
import time

from lib import ControlThread, ControlSystem

@ControlThread
def imu_sensor():
    
    import math
    from Adafruit_BNO055.BNO055 import BNO055 as Bno
    bno = Bno(serial_port='/dev/ttyUSB1')
    if not bno.begin():
        raise RuntimeError('BNO sensor not connected')
    
    while True:
        h, r, p = bno.read_euler()
        x, y, z = bno.read_linear_acceleration()
        lin_acc = math.sqrt((x**2) + (y**2) + (z**2))
        ControlSystem().post(imu_lin_acc=lin_acc, imu_heading=h)
        time.sleep(0.1)

@ControlThread
def gps_sensor():
    
    import gpsd
    gpsd.connect()
    gpsd.connect(host='localhost', port=2947)
    
    while True:
        try:
            newlat, newlon = gpsd.get_current().position()
            ControlSystem().post(lat=newlat, lon=newlon)
        except:
            pass

@ControlThread
def write_sensors(imu_lin_acc, imu_heading, lat, lon):
    while True:
        ControlSystem().console.log('values for imu: ({0}, {1}), values for gps: ({2}, {3})'.format(
            str(imu_lin_acc), str(imu_heading), str(lat), str(lon)))

ControlSystem().openConsole()
