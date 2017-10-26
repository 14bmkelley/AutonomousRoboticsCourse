# Using the IMU Sensor

Before beginning, please review [an article](https://learn.adafruit.com/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black) about interfacing the BNO055 IMU sensor with a Raspberry Pi.

Using the code provided in the article, create a control thread on the
Raspberry Pi that reads the IMU sensor data. Use the following snippet
to initialize and emit sensor data.

```python

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
