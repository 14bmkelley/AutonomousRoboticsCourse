import AutonomousRoboticsCourse

if __name__ == '__main__':

    def onTrigger_gps(device, xPos, yPos, zPos):
        print('x = {0}, y = {1}, z = {2}'.format(xPos, yPos, zPos))

    device = AutonomousRoboticsCourse.initialize()
    AutonomousRoboticsCourse.NetworkAdapter(device)

    device.onTrigger['gps'] = onTrigger_gps

    device.trigger('gps', xPos=1, yPos=2, zPos=3)
    device.trigger('send', 'item')

