
import time
from math import radians, pow, sin, cos, atan2, degrees

from arc.core import ControlThread, system

def geo_vector(lat1, long1, lat2, long2, typeof):

    if typeof == 'I':
        return -1, -1

    my_location = (lat1, long1)
    target = (lat2, long2)
    radius = 6371000

    lat1 = math.radians(my_location[0])
    lat2 = math.radians(target[0])

    diffLat = lat2 - lat1
    diffLong = radians(target[1] - my_location[1])

    a = pow(sin(diffLat / 2), 2) + cos(lat1) * cos(lat2) * pow(sin(diffLong / 2), 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = radius * c

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(diffLong)
    initial_bearing = degrees(atan2(x, y))
    compass_bearing = (initial_bearing + 360) % 360

    if typeof == 'B':
        compass_bearing = compass_bearing + 180
        if compass_bearing >= 360:
            compass_bearing = compass_bearing - 360

    return distance, compass_bearing

@ControlThread
def imu():
    
    import math
    from Adafruit_BNO055.BNO055 import BNO055 as Bno
    bno = Bno(serial_port='/dev/ttyUSB1')
    if not bno.begin():
        raise RuntimeError('BNO sensor not connected')
    
    while system.active:
        h, r, p = bno.read_euler()
        x, y, z = bno.read_linear_acceleration()
        lin_acc = math.sqrt((x**2) + (y**2) + (z**2))
        system.post(imu_lin_acc=lin_acc, imu_heading=h)

@ControlThread
def gps():
    
    import gpsd
    gpsd.connect()
    gpsd.connect(host='localhost', port=2947)
    
    while system.active:
        try:
            newlat, newlon = gpsd.get_current().position()
            system.post(lat=newlat, lon=newlon)
        except:
            pass

@ControlThread
def target():
    while True:
        system.post(target_lat=0, target_lon=0)
        time.sleep(0.2)

@ControlThread
def move_robot(imu_lin_acc, imu_heading, lat, lon, target_lat, target_lon):
    
    while lat.value != target_lat.value and lon.value != target_lon.value:
        
        imu_lin_acc = imu_lin_acc.value
        imu_heading = imu_heading.value
        lat = lat.value
        lon = lon.value
        target_lat = target_lat.value
        target_lon = target_lon.value
        
        dist, heading = geo_vector(lat, lon, target_lat, target_lon, 'F')
        m0, m1 = heading_controller(float(imu_heading), float(heading))
        control_motor(0, m0)
        control_motor(1, m1)
        time.sleep(0.1)



system.hold(console=True)

