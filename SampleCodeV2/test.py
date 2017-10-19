
###
# Sample user file.
###

import time

from lib import ControlThread, ControlSystem

@ControlThread
def sensor1():
    x = 1
    while True:
        ControlSystem().post(hello1='world {0}'.format(x))
        x += 1
        time.sleep(0.1)

@ControlThread
def sensor2():
    y = 1
    while True:
        ControlSystem().post(hello2='world {0}'.format(y))
        y += 1
        time.sleep(0.4)

@ControlThread
def controller(hello1, hello2):
    while True:
        ControlSystem().console.log('hello1 = ' + str(hello1.value)
                + ', hello2 = ' + str(hello2.value), tag='controller')
        time.sleep(0.5)

ControlSystem().openConsole()

