
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


def read_calibration(bno):
    if 'imu_save_state.data' in os.listdir():
        with open('imu_save_state.data', 'rb') as imu_save_state:
            data = [ int(d) for d in imu_save_state.readline().split('') ]
            bno.set_calibration(data)

def write_calibration(bno):
    with open('imu_save_state.data', 'wb') as imu_save_state:
        data = bno.get_calibration()
        for value in data:
            imu_save_state.write('%d' % value)

@ControlThread
def imu_sensor(imu_enable):
    
    import math
    from Adafruit_BNO055.BNO055 import BNO055 as Bno
    bno = Bno(serial_port='/dev/ttyUSB1')
    if not bno.begin():
        raise RuntimeError('BNO sensor not connected')

    read_calibration(bno)

    while system.active:
        if imu_enable.value == 'True':
            h, r, p = bno.read_euler()
            x, y, z = bno.read_linear_acceleration()
            lin_acc = math.sqrt((x**2) + (y**2) + (z**2))
            system.post(imu_lin_acc=lin_acc, imu_heading=h)
        else:
            time.sleep(0.1)

    write_calibration(bno)

@ControlThread
def gps_sensor(gps_enable):
    
    import gpsd
    gpsd.connect()
    gpsd.connect(host='localhost', port=2947)
    
    while system.active:
        if gps_enable.value == 'True':
            try:
                newlat, newlon = gpsd.get_current().position()
                system.post(lat=newlat, lon=newlon)
            except:
                pass
        time.sleep(0.1)

def clamp(value, min, max):
    if value > max:
        value = max
    if value < min:
        value = min
    return value

@ControlThread
def motor_control(motor_rspeed, motor_lspeed):

    import serial

    port = serial.Serial('/dev/ttyUSB2', baudrate=9600, timeout=3.0)
    port.write(bytearray([0xAA]))

    while system.active:

        if motor_rspeed.value == None or motor_lspeed.value == None:
            time.sleep(0.1)
            continue

        rspeed = int(1.27 * clamp(int(motor_rspeed.value), -100, 100))
        lspeed = int(1.27 * clamp(int(motor_lspeed.value), -100, 100))

        if rspeed > 0:
            port.write(bytearray([0x88, rspeed1]))

        if lspeed > 0:
            port.write(bytearray([0x8C, rspeed2]))

        if rspeed < 0:
            port.write(bytearray([0x8A, abs(rspeed1)]))

        if lspeed < 0:
            port.write(bytearray([0x8E, abs(rspeed1)]))

        else:
            port.write(bytearray([0x86, 0]))
            port.write(bytearray([0x87, 0]))

        time.sleep(0.1)

@ControlThread
def move_robot(imu_lin_acc, imu_heading, lat, lon, target_lat, target_lon):
    
    while lat.value != target_lat.value and lon.value != target_lon.value:
        
        imu_lin_acc = imu_lin_acc.value
        imu_heading = imu_heading.value
        lat = lat.value
        lon = lon.value
        target_lat = target_lat.value
        target_lon = target_lon.value
        
        if target_lat == None or target_lon == None:
            time.sleep(0.1)
            continue

        target_lat = int(target_lat)
        target_lon = int(target_lon)

        dist, heading = geo_vector(lat, lon, target_lat, target_lon, 'F')
        m0, m1 = heading_controller(float(imu_heading), float(heading))
        system.post(motor_rspeed=m0, motor_lspeed=m1)
        time.sleep(0.1)



system.hold(console=True)

