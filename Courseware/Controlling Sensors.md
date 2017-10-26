# Reading From Sensors

In this exercise, you will apply a multithreading framework to read
sensor data from IMU and GPS sensors on a Raspberry Pi. The BNO055
Inertial Measurement Unit (IMU) is used to determine orientation and
the Adafruit Ultimate GPS Breakout board, to determine location.

Please review [an article](https://learn.adafruit.com/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black) about
setting up and interfacing the BNO055 IMU sensor with a Raspberry Pi.

In addition, read [this article](https://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi/setting-everything-up?view=all) to
learn about setting up and interfacing the Adafruit Ultimate GPS
sensor.

### Defining sensor functions

Using the code provided in the articles, create two control threads on
the Raspberry Pi, one to read IMU sensor data and the other to read
GPS sensor data. This can be done by defining two functions, each with
the ControlThread decorator, which will serve as the lifetime of the
sensor. Within each function, initialize and begin continuously
updating data using the ```ControlSystem().post()``` function. A
sample function template is shown below.

```python

from AutonomousRoboticsCourse import ControlThread, ControlSystem

@ControlThread
def imu_sensor():
   
   #####
   # Fill in the code to initialize the IMU sensor below.
   #####


   while True:

      #####
      # Fill in the code to continually read IMU sensor data.
      #####


      # Post the sensor data as key-value pairs.
      ControlSystem().post(key1 = value1, key2 = value2)

```

### Testing sensor functions

Sensor values can be verified using a terminal connection. This can be
done by calling ```ControlSystem().openConsole()``` while a control
thread is running. The console is capable of sorting traffic from
multiple posting threads and aggregate them using tag filtering
commands.


