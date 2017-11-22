
import time

from arc.core import ControlThread, system

@ControlThread
def gps_sensor():
    
    import gpsd
    gpsd.connect()
    gpsd.connect(host='localhost', port=2947)
    
    while system.active:
        try:
            lat, lon = (gpsd.get_current()).position()
            system.post(lat=lat, lon=lon)
        except:
            pass
        time.sleep(0.1)

@ControlThread
def logging(lat, lon):
    
    while system.active:
        system.console.log('lat: {0}, lon: {1}'.format(str(lat), str(lon)))
        time.sleep(0.2)

system.hold(console=True)

