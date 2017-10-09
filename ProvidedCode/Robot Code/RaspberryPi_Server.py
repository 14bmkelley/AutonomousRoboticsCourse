#!/usr/bin/python

##################################################################
# Name: pyserver.py
# Desc: Opens port 334411 on localhost and waits for connections
# Credit: Source adapted from python server on http://stackoverflow.com/questions/25787944/python-socket-server-to-php-client-socket
#       Changes made to remove logging, fix connect bug (as 
#       described at source), and print to stderr.
# Intent: Modify below to act as a python command server for 
#         your PHP website
# Author: adanowit@calpoly.edu
#################################################################

import socket
import time
import sys
import json

import gps


import logging
from Adafruit_BNO055 import BNO055
bno = BNO055.BNO055(serial_port='/dev/ttyUSB0')




#GPIO_Function***************************************************

"""

def handle_gpio(cmd):	## Notice that we call the function and use the arguments and commands in the pyserver.py file

    
    #Python doesn't seem to have case statments,
    #so implement as an if-elif-else
    resp = -1
    
    if cmd['cmd'] == 'MODE':					##MODE is a gpio command
        if cmd['arg'] == 'BCM':					##BCM is an gpio argument
            resp = GPIO.setmode(GPIO.BCM)
        else :
            resp = GPIO.setmode(GPIO.BOARD)
    elif cmd['cmd'] == 'INPUT':					
        resp = GPIO.setup(cmd['arg'], GPIO.IN)	
    elif cmd['cmd'] == 'OUTPUT':
        resp = GPIO.setup(cmd['arg'], GPIO.OUT)
    elif cmd['cmd'] == 'READ':
        resp = GPIO.input(cmd['arg'])
    elif cmd['cmd'] == 'WRITE1':
        resp = GPIO.output(cmd['arg'], 1)
    elif cmd['cmd'] == 'WRITE0':
        resp = GPIO.output(cmd['arg'], 0)
    else:
        sys.stderr.write("Error, command " + str(cmd['cmd']) + " not found\n")
        sys.exit(1)

    return {'resp':resp}
    
"""

#GPIO_Function_End***************************************************







#IMU_Function*******************************************************

# Enable verbose debug logging if -v is passed as a parameter.

if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)
 
# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

def handle_IMU(cmd):	## Notice that we call the function and use the arguments in the pyserver.py file

    
    #Python doesn't seem to have case statments,
    #so implement as an if-elif-else
    resp = -1
        
    if cmd['cmd'] == 'EULER':		##EULER is an IMU sensor command
        resp = bno.read_euler()
    elif cmd['cmd'] == 'CALIB':		##CALIB is an IMU sensor command
        resp = bno.get_calibration_status()
        
    else:
        sys.stderr.write("Error, command " + str(cmd['cmd']) + " not found\n")
        sys.exit(1)

    return {'resp':resp}


#IMU_Function_End*******************************************************






#GPS_Function********************************************************

def handle_GPS(cmd):
	
	##initialize GPS before use
	
    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    resp = -1

    while (resp == -1):
        try:
            report = session.next()
		# Wait for a 'TPV' report and display the current time
		# To see all report data, uncomment the line below
		# print report
            if report['class'] == 'TPV':
                if cmd['cmd'] == 'LAT' :
                    if hasattr(report, 'lat'):
                        resp = report.lat
                    else:
                        resp = -1
                    #    sys.stderr.write("Error, command " + str(cmd['cmd']) + " not found\n")
                    #    sys.exit(1)

                elif cmd['cmd'] == 'LONG':
                    if hasattr(report,'lon'):
                        resp = report.lon
                else:
                    sys.stderr.write("Error, command " + str(cmd['cmd']) + " not found\n")
                    sys.exit(1)

        except KeyError:
                    pass
        except KeyboardInterrupt:
                    quit()
        except StopIteration:
                    session = None
                    print "GPSD has terminated"

    return {'resp':resp}
    
    
#GPS_Function_End***************************************************







#Connect_Function****************************************************

def connect():
    HOST = '127.0.0.1' #We're keeping things local, so use localhost's IP!
    PORT = '334411' #Random port above 1024 (unprivileged). Read as EE 4 All

    sock = None

    for result in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = result

        try: #Try to create the socket
            sock = socket.socket(af, socktype, proto)
        except socket.error, msg:
            sys.stderr.write('Socket Error Code : ' + str(msg[0]) + ' Message ' + msg[1]) #print error if it fails
            sock = None
            continue

        try: #Try to bind to the socket
            sock.bind(sa)
            sock.listen(1)
        except socket.error, msg:
            sys.stderr.write('Socket bind/listening Error Code : ' + str(msg[0]) + ' Message ' + msg[1])     
            sock.close() #close the socket
            sock = None
            continue
        break

    if sock is None:
        sys.stderr.write("could not open socket")
        sys.exit(1)

    #########################################################################
    #Server handling portion
    #########################################################################
    #Wait for a socket connection from PHP
    while True:
        
        ##----------------------------------------------------
        
        conn, addr = sock.accept()
    
        #Loop on requests from php. PHP can break connection with command
        #"end_session."
        while True:
            data = conn.recv(1024) #Grab 1024 bytes from the socket
		
		##----------------------------------------------------
		
		
            #print to the command line (debugging)
            #sys.stderr.write("\nGot data: " +str(data) + "\n")
            

            ####
            # Try to interpret command as json. If a non-json command is
            # recieved, close the connection.
            ####
            try:
                cmd = json.loads(data)
            except ValueError:
                sys.stderr.write("Client sent non-json data. This may occur "+\
                                 "if client closed socket without sending "+\
                                 "'end_session' command")
                break
            
            #If we reiceve the "end_session" close the connection
            if (cmd == "end_session"):
                break

            #Default "op failed" return value
            ret_val = {'resp':-1}

            ##################################
            # Code handling: This file only takes and routes requests
            # to the appropriate python modules. Add code here to
            # accept more command types!
            ##################################
            
##---------------------------------------------------------

            if cmd['type'] == 'IMU':
                #sys.stderr.write("Got IMU command!\n")
                ret_val = handle_IMU(cmd)
                
            
                
            elif cmd['type'] == 'GPS':
				#sys.stderr.write("Got IMU command!\n")
                ret_val = handle_GPS(cmd)
          
            #Convert the return value back into json
            ret_json = json.dumps(ret_val)

            #sys.stderr.write("\nSent data: " + ret_json + "\n")
            #send the return value back to the requester (php)
            conn.send(str(ret_json))
            
##---------------------------------------------------------

        
        # Once the client has closed its session, close the connection and
        # loop back to wait for new connection requests
        # conn.close() --- keep the connection to read more data
        
#Connect_Function_End****************************************************



if __name__=="__main__":
    connect()
