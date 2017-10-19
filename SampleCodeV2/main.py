
import time

from lib import ControlThread, ControlSystem

@ControlThread
def imu():
    import math
    from Adafruit_BNO055 import BNO055 as bno_lib
    bno = BNO055.BNO055(serial_port='/dev/ttyUSB2')
    if not bno.begin():
        raise RuntimeError('BNO sensor not connected')
    while True:
        h, r, p = bno.read_euler()
        x, y, z = bno.read_linear_acceleration()
        lin_acc = math.sqrt((x**2) + (y**2) + (z**2))
        ControlSystem().post(imu_lin_acc=lin_acc, imu_heading=h)

@ControlThread
def gps():
    import gps
    session = gps.gps('localhost', '2947')
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    while True:
        report = session.next()
        ControlSystem().post(lat=report.lat, lon=report.lon)

@ControlThread
def move_robot(imu_lin_acc, imu_heading, lat, lon, target_lat, target_lon):
    while lat != target_lat and lon != target_lon:
        dist, heading = geo_vector(lat, lon, target_lat, target_lon, 'F')
        m0, m1 = heading_controller(float(imu_heading), float(heading))
        control_motor(0, m0)
        control_motor(1, m1)
        time.sleep(0.1)

ControlSystem().openConsole()

