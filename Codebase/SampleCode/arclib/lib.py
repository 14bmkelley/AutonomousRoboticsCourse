
from .core import ControlThread, system

def navigate(startlat, startlon, endlat, endlon):

    system.postlink(startlat, 'startlat')
    system.postlink(startlon, 'startlon')
    system.postlink(endlat, 'endlat')
    system.postlink(endlon, 'endlon')

    @ControlThread
    navigateControlThread(startlat, startlon, endlat, endlon):
        

