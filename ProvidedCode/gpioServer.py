#####################################################
#
# Expected data structure
#
# Dict: {'type':'GPIO', 'cmd':'STRING WITH ALLOWABLE COMMAND', 'args': 'COMMAND SPECIFIC ARGS'}
# Command :: arg :: Definition
# INPUT :: <pin_num> :: Sets pin <pin_num> to input
# OUTPUT :: <pin_num> :: Sets pin <pin_num> to output
# READ :: <pin_num> :: Read and return value on <pin_num>
# WRITE1 :: <pin_num> :: Write 1 on <pin_num>
# WRITE0 :: <pin_num> :: Write 0 on <pin_num>
# MODE :: <BCM or BOARD> :: Sets addressing mode for pi, either using
#                           the broadcomm pin nums, or the board pin nums
#####################################################
import sys

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    sys.stderr.write("Error, unable to import GPIO. Are you running with adminstrative privileges?")
    sys.exit(1)

def handle_gpio(cmd):

    
    #Python doesn't seem to have case statments,
    #so implement as an if-elif-else
    resp = -1
    
    if cmd['cmd'] == 'MODE':
        if cmd['arg'] == 'BCM':
            resp = GPIO.setmode(GPIO.BCM)
        else :
            resp = GPIO.setmode(GPIO.BOARD)
    elif cmd['cmd'] == 'INPUT':
        resp = GPIO.setup(cmd['arg'], GPIO.IN)
    elif cmd['cmd'] == 'OUTPUT':
        resp = GPIO.setup(cmd['arg'], GPIO.OUT)
    elif cmd['cmd'] == 'READ':
        resp = GPIO.input(cmd['arg'])
    elif cmd['cmd'] == 'WRITE1':
        resp = GPIO.output(cmd['arg'], 1)
    elif cmd['cmd'] == 'WRITE0':
        resp = GPIO.output(cmd['arg'], 0)
    else:
        sys.stderr.write("Error, command " + str(cmd['cmd']) + " not found\n")
        sys.exit(1)

    return {'resp':resp}
