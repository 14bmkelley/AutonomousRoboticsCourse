
###
# Sample user file.
###

import time

from arc.core import ControlThread, system

@ControlThread
def sensor1(hello1):

    postit = 1

    while system.active:

        if hello1.value != None:
            postit += 1

        if isinstance(hello1.value, str):
            postit = 1

        system.post(hello1=postit)
        time.sleep(0.05)

@ControlThread
def sensor2():
    y = 1
    while system.active:
        system.post(hello2='world {0}'.format(y))
        y += 1
        time.sleep(0.05)

@ControlThread
def controller(hello1, hello2):
    system.postlink('hello1', 'linked')
    while system.active:
        system.console.log('hello1 = ' + str(hello1.value)
                + ', hello2 = ' + str(hello2.value), tag='controller')
        time.sleep(0.1)

@ControlThread
def linktest(templink):
    while system.active:
        if linked.value != None:
            system.console.log('hello1: {0}, linked: {1}'.format(
                str(hello1), str(linked)))
        time.sleep(0.1)

system.hold(console=True)

