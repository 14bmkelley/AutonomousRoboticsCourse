import serial
import logging
import sys
import time
from math import *
global Kp
global Ki
Kp, Ki = 0.1, 0.1


port = serial.Serial("/dev/ttyUSB1", baudrate=9600, timeout=3.0)
port.write(bytes([0xAA]))
     
from Adafruit_BNO055 import BNO055
bno = BNO055.BNO055(serial_port='/dev/ttyUSB2')
# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)
 
# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')


#Initialize the controller with 0xAA (for automatic baud detection)
def Move(Error):
    speed = Error
    pwm_1=int(speed*(127.0/100.0))
        # Motor goes full speed
    if (pwm_1>0 and pwm_1<=64):
            #pwm_1 = (pwm_1)
        port.write(bytes([0x88, pwm_1]))
        print('Motor Speed={0:0.2F}'.format(pwm_1))
    elif (pwm_1>64 and pwm_1<=127):
        port.write(bytes([0x89, (pwm_1)]))
        print('Motor Speed={0:0.2F}'.format(pwm_1))
    elif (pwm_1<0 and pwm_1>=-64):
        port.write(bytes([0x8A, -pwm_1]))
        print('Motor Speed={0:0.2F}'.format(-pwm_1))
    elif (pwm_1<-64 and pwm_1>=-127):
        port.write(bytes([0x8B, (-pwm_1)]))
        print('Motor Speed={0:0.2F}'.format(-pwm_1))
    elif (pwm_1 == 0):
        port.write(bytes([0x88, 0x00]))
        print('Motor Speed={0:0.2F}'.format(pwm_1))
            

    pwm_2=int(speed*(127.0/100.0))
        # Motor goes full speed
    if (pwm_2>0 and pwm_2<=64):
            #pwm_1 = (pwm_1)
        port.write(bytes([0x8C, pwm_2]))
        print('Motor Speed={0:0.2F}'.format(pwm_2))
    elif (pwm_2>64 and pwm_2<=127):
        port.write(bytes([0x8D, (pwm_2)]))
        print('Motor Speed={0:0.2F}'.format(pwm_2))
    elif (pwm_2<0 and pwm_2>=-64):
        port.write(bytes([0x8E, -pwm_2]))
        print('Motor Speed={0:0.2F}'.format(-pwm_2))
    elif (pwm_2<-64 and pwm_2>=-127):
        port.write(bytes([0x8F, (-pwm_2)]))
        print('Motor Speed={0:0.2F}'.format(-pwm_2))
    elif (pwm_2 == 0):
        port.write(bytes([0x8C, 0x00]))
        print('Motor Speed={0:0.2F}'.format(pwm_2))



def Heading():
    # Print system status and self test result.
    status, self_test, error = bno.get_system_status()
    print('System status: {0}'.format(status))
    print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
    # Print out an error if system status is in error mode.
    if status == 0x01:
        print('System error: {0}'.format(error))
        print('See datasheet section 4.3.59 for the meaning.')
         
    # Print BNO055 software revision and other diagnostic data.
    sw, bl, accel, mag, gyro = bno.get_revision()
    print('Software version:   {0}'.format(sw))
    print('Bootloader version: {0}'.format(bl))
    print('Accelerometer ID:   0x{0:02X}'.format(accel))
    print('Magnetometer ID:    0x{0:02X}'.format(mag))
    print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

    print('Reading BNO055 data, press Ctrl-C to quit...')
    d_heading = raw_input("Enter Desired Heading :")
    d_heading = radians(float(d_heading))
    accum_error = 0
    while True:
        # Read the Euler angles for heading, roll, pitch (all in degrees).
        heading, roll, pitch = bno.read_euler()
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
        #sys, gyro, accel, mag = bno.get_calibration_status()
        # Print everything out.
        print('\n')
        print('Heading={0:0.2F}'.format(heading))
        heading = radians(float(heading))
        Error = atan2(sin(d_heading - heading),cos(d_heading - heading))
        accum_error = Kp * Error + accum_error
        output = Ki * Error + accum_error
        print('Error in degrees={0:0.2F}'.format(degrees(Error)))
        print('PID Output={0:0.2F}'.format(degrees(output)))
        Move(degrees(output))
        
if __name__=="__main__":        
    while True:
        Heading()
