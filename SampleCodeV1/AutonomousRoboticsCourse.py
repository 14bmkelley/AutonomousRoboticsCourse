

class NetworkAdapter:

    def __init__(self, autonomousRobot):
        autonomousRobot.onTrigger['send'] = NetworkAdapter.send
        autonomousRobot.onTrigger['receive'] = NetworkAdapter.receive

    @staticmethod
    def send(autonomousRobot, obj):
        print('hello world!')
    
    @staticmethod
    def receive(autonomousRobot, obj):
        pass


class AutonomousRobot:

    def __init__(self):
        self.onTrigger = {}

    def trigger(self, eventName, *args, **kwargs):
        if eventName in self.onTrigger:
            self.onTrigger[eventName](self, *args, **kwargs)



connectedDevice = None

def initialize():
    connectedDevice = AutonomousRobot()
    return connectedDevice

def instance():
    if connectedDevice == None or not connectedDevice.valid:
        connectedDevice = AutonomousRobot()
    return connectedDevice

