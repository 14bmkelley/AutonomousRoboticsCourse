import serial
 
port = serial.Serial("/dev/ttyUSB1", baudrate=9600, timeout=3.0)
 
port.write('AA'.decode("hex"))
 
while True:
        rotation=int(raw_input('Please enter a rotational velocity from -127 to 127:')) 
        speed=int(raw_input('Please enter a forward velocity from -127 to 127:'))
        rightmotor=rotation+speed
        leftmotor=rotation-speed
        if rightmotor>127:
                rightmotor=127
        if rightmotor<-127:
                rightmotor=-127
        if leftmotor>127:
                leftmotor=127
        if leftmotor<-127:
                leftmotor=-127
        if leftmotor>=0:
                port.write('8E'.decode("hex"))
                port.write(chr(leftmotor))
        else:
                port.write('8C'.decode("hex"))
                port.write(chr(-leftmotor))
        if rightmotor>=0:
                port.write('8A'.decode("hex"))
                port.write(chr(rightmotor))
        else:
                port.write('88'.decode("hex"))
                port.write(chr(-rightmotor))
