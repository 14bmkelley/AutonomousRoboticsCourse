import AutonomousRoboticsCourse
#import gps

if __name__ == '__main__':

    device = AutonomousRoboticsCourse.initialize()

    def onTrigger_log(device, message):
        device.foreground(target = lambda: print(message))
    
    device.onTrigger['log'] = onTrigger_log

    def onTrigger_gps(device):
        
        #import gps
        
        #session = gps.gps('localhost', '2947')
        #session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

        #report = None

        #while report = session.next():
        for i in range(10):
            #device.trigger('log', 
            #        'lat = {0}, lon = {1}'.format(report.lat, report.lon))
            device.trigger('log',
                    'lat = {0}, lon = {1}'.format(i, 0))
        
        device.trigger('gps-complete')

    device.onTrigger['gps'] = onTrigger_gps
    device.trigger('gps', async=True)

    device.background()

    print('complete')

