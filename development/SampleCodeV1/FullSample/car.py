import AutonomousRoboticsCourse
import gps



# Get an instance of the device this code will run on.
device = AutonomousRoboticsCourse.initialize()



# Define a function to log messages to the console on
# the main thread and bind it to the onTrigger list.
def onTrigger_log(device, message):
    device.foreground(target = lambda: print(message))

device.onTrigger['log'] = onTrigger_log



# Define a function to emit GPS locations on every
# report session and bind it to the onTrigger list.
# Then, trigger it as an asynchronous event that will
# produce other events (individual GPS reports).
def onTrigger_gps(device):
        
    import gps
        
    session = gps.gps('localhost', '2947')
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    report = None

    while report = session.next():
        device.trigger('log', 
                'lat = {0}, lon = {1}'.format(report.lat, report.lon))
        
device.onTrigger['gps'] = onTrigger_gps
device.trigger('gps', async=True)



# Whenever the device is ready to read signals,
# background the main thread and wait.
device.background()

print('autonomous program complete')

