
import time

from lib import ControlThread, ControlSystem

@ControlThread
def gps_sensor():
    
    import gpsd
    gpsd.connect()
    gpsd.connect(host='localhost', port=2947)
    #session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    
    while True:
        try:
            report = gpsd.get_current()
            ControlSystem().post(pos=report.position())
        except:
            pass
        time.sleep(0.1)

@ControlThread
def logging(pos):
    while True:
        if pos.value == None:
            continue
        lat, lon = pos.value
        ControlSystem().console.log('lat: {0}, lon: {1}'.format(str(lat), str(lon)))
        time.sleep(0.2)

ControlSystem().openConsole()
