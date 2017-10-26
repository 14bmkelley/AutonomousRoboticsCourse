
import threading as th

##########################################################################
# Data structures
##########################################################################



class CheckThread(th.Thread):

    def __init__(self, *args, **kwargs):
        super(CheckThread, self).__init__(*args, **kwargs)
        self._stopEvent = th.Event()

    def _stopThread(self):
        self._stopEvent.set()

    def _isStoppedThread(self):
        return self._stopEvent.is_set()



###
# NetworkAdapter
# This class modifies an AutonomousRobot to support send and receive
# operations over a network connection.
###
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



###
# AutonomousRobot
# This class represents a device that functions autonomously by triggering
# and responding to events.
###
class AutonomousRobot:

    def __init__(self):
        self.onTrigger = {}
        self.blocking = False
        self._mainThreadRequests = []
        self._runningThreads = []
        self._runningThreadsReorg = False

    ###
    # This function attempts to trigger an event that can be either a one-
    # off execution or a background thread that periodically reports.
    ###
    def trigger(self, eventName = None, target = None, *args, **kwargs):

        state = self._triggerDetermineState(eventName, target, args, kwargs)

    def _triggerDetermineState(self, eventName, target, *args, **kwargs):

        if eventName is not None and target is None and 

    def trigger(self, eventName, *args, **kwargs):

        # If this event doesn't exist, just raise an exception
        if eventName not in self.onTrigger:
            raise Exception('AutonomousRoboticsCourse: Event not found.')

        # If the event's callable function isn't callable, just raise an
        # exception.
        elif not callable(self.onTrigger[eventName]):
            raise Exception('AutonomousRoboticsCourse: Event function not \
                    callable')

        # If the event exists as an asynchronous caller, start a thread.
        elif 'async' in kwargs and kwargs['async'] is True:
            del kwargs['async']
            newThread = CheckThread(name = eventName,
                                    target = self.onTrigger[eventName],
                                    args = (self,) + args,
                                    kwargs = kwargs)
            self.onTrigger[eventName + '-complete'] = self._completeThread(newThread)
            newThread.daemon = True
            newThread.start()
            self._runningThreads.append(newThread)
            # Attempt to reorganize threads if one is added.
            if not self._runningThreadsReorg:
                self._runThreadsReorg()

        # If the event exists, but it is a one-off, just execute it.
        else:
            self.onTrigger[eventName](self, *args, **kwargs)

    def background(self):
        self.blocking = True
        while (self.blocking):
            if len(self._mainThreadRequests) > 0:
                request = self._mainThreadRequests.pop()
                if callable(request):
                    result = request()
                    if isinstance(result, Exception):
                        raise result
                elif type(result) in [ list, tuple ]:
                    self.trigger(result[0], result[1], result[2])

    def foreground(self, eventName = None, *args, **kwargs, target = None):
        if eventName is not None:
            self._mainThreadRequests.append((eventName, args, kwargs))
        elif not not target and callable(target):
            self._mainThreadRequests.append(target)
        elif not not target:
            self._mainThreadRequests.append(lambda: Exception(
                'AutonomousRoboticsCourse: func argument is not callable.'))
        else:
            self.blocking = False

    # Remove unused threads.
    def _runThreadsReorg(self):
        self._runningThreadsReorg = True
        for thread in self._runningThreads:
            if thread._isStoppedThread():
                self.trigger(thread.getName() + '-complete')
                self._runningThreads.remove(thread)
        self._runningThreadsReorg = False

    def _completeThread(self, thread):
        return lambda _: thread._stopThread()



#########################################################################
# Library setup
#########################################################################

# Create an instance of AutonomousRobot for every device that uses this
# library.
connectedDevice = None

# Instantiate a new autonomous robot EVERY time this function is called to
# represent the device using this library.
def initialize():
    connectedDevice = AutonomousRobot()
    return connectedDevice

# Get an instance of the current autonomous robot device using the library.
def instance():
    if connectedDevice == None or not connectedDevice.valid:
        connectedDevice = AutonomousRobot()
    return connectedDevice

