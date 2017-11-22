
import collections
import threading
import re
import sys




'''
A Python class implementing KBHIT, the standard keyboard-interrupt poller.
Works transparently on Windows and Posix (Linux, Mac OS X). Doesn't work
with IDLE.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
'''

import os

# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select

class KBHit:

    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        if os.name == 'nt':
            pass

        else:

            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)

    def set_normal_term(self):
        ''' Resets to normal terminal. On Windows this is a no-op.
        '''

        if os.name == 'nt':
            pass

        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''

        s = ''

        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')

        else:
            return sys.stdin.read(1)

    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''

        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]

        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]

        return vals.index(ord(c.decode('utf-8')))

    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()

        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []



        

class ControlWrapper:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value.__str__()





class Console:

    def __init__(self):
        self._tagSettings = { 'untagged': True }
        self._tagSettingsLock = threading.Lock()
        self._output = collections.deque([])
        self._outputLock = threading.Lock()
        self._outputHandler = sys.stdout
        self._kb = KBHit()
        self.active = True

    def start(self):
        self.active = True
        self._log('\nConnecting to console...\n')

    def stop(self):
        self.active = False

    def log(self, message='', tag=None, tags=None, end='\n'):
        
        # Restrictions made on outside users.
        if tag == None and tags == None:
            tag = 'untagged'

        self._log(message, tag, tags, end)

    def _log(self, message='', tag=None, tags=None, end='\n'):

        if not self.active:
            return

        buffered = False

        if end == '\r':
            end = ''
            buffered = True

        message += end

        with self._outputLock:

            if tag == None and tags == None:
                self._output.append(( str(message), buffered ))

            elif tag == 'untagged' and self._tagSettings['untagged']:
                self._output.append(( str(message), buffered ))

            elif tag != None and isinstance(tag, str):
                if tag in self._tagSettings and self._tagSettings[tag]:
                    self._output.append(( tag + ': ' + str(message),
                        buffered ))
                else:
                    with self._tagSettingsLock:
                        self._tagSettings[tag] = False

            elif tags != None and isinstance(tags, list):

                currentSettings = filter(lambda tup: tup[0] in tags and tup[1] == True,
                    self._tagSettings.items())
            
                for tagName, _ in currentSettings:
                    self._output.append(( tagName + ': ' + str(message), 
                        buffered ))

                unsetSettings = filter(lambda tag: tag not in self._tagSettings, tags)
            
                with self._tagSettingsLock:
                    for tagName in unsetSettings:
                        self._tagSettings[tagName] = False

            else:
                pass # Oops

    def readline(self):

        if not self.active:
            return

        buf = '(press ctrl+c to stop) $> '
        uneditLen = len(buf)
        lineComplete = False
        
        # Collect an entire line.
        while not lineComplete:

            self._log(buf, end='\r')

            # Buffer next input if possible.
            if self._kb.kbhit():
                buf += self._kb.getch()
            
            # Remove previous character if a backspace is processed.
            if buf[-1] == '\x7f':
                if len(buf) > uneditLen + 1:
                    buf = re.sub('.{1}\x7f', '', buf, count=1)
                buf = re.sub('\x7f', '', buf)

            # If a line is completed with a newline.
            if buf[-1] == '\n':
                self._log(buf)
                lineComplete = True

        buf = buf[:-1]
        tokens = buf.split(' ')
        args = buf.split(' ')[5:]
        self.processTokens(args)
        self._log()

    def processTokens(self, tokens):
        if hasattr(self, tokens[0]):
            args = []
            if len(tokens) > 1:
                args = tokens[1:]
            else:
                pass
            getattr(self, tokens[0])(*args)

    def setOutputHandler(obj):
        self._outputHandler = obj

    def help(self, *args):
        self._log('Enter "help" to see the help menu.')

    def setTag(self, *args):
        if len(args) > 0:
            with self._tagSettingsLock:
                self._tagSettings[args[0]] = True
                self._log('"' + args[0] + '" tag set.')

    def unsetTag(self, *args):
        if len(args) > 0:
            with self._tagSettingsLock:
                self._tagSettings[args[0]] = False
                self._log('"' + args[0] + '" tag unset.')

    def showTags(self, *args):
        if len(self._tagSettings) == 0:
            self._log('No tags available.')
        else:
            self._log('Tag                  Status')
            self._log('==============================================')
            for tag, status in self._tagSettings.items():
                self._log('{:20} '.format(tag) + str(status))






def Locker(func, lock):
    def lockedFunc():
        with lock:
            func()
    return lockedFunc

class ControlSystemInterface:

    def __init__(self):
        self._controlValues = dict()
        self._controlValuesLock = threading.Lock()
        self._threads = list()
        self.active = True
        self.console = Console()
        self.console.stop()

    def post(self, **kwargs):
        with self._controlValuesLock:
            for k, v in kwargs.items():
                self.console.log('key value pair updated: ({0}, {1})'.format(
                    str(k), str(v)), tags=['_internal', '_onPost'])
                if k in self._controlValues:
                    self._controlValues[k].value = kwargs[k]
                else:
                    self._controlValues[k] = ControlWrapper(kwargs[k])

    def postlink(self, key, linkkey):
        with self._controlValuesLock:
            if key not in self._controlValues:
                self._controlValues[key] = ControlWrapper(None)
            self._controlValues[linkkey] = self._controlValues[key]

    def unpost(self, key):
        with self._controlValuesLock:
            if key in self._controlValues:
                del self._controlValues[key]

    def hold(self, console=False):

        import time
        
        try:
            
            if console:
                self.console.start()

            while True:
                if console:
                    self.console.readline()
                else:
                    time.sleep(100)
        
        except KeyboardInterrupt:
            
            self.active = False
            if console:
                self.console.stop()
            
            print('\n<ctrl+c>\n\nStopping now...')
            
            for thread in self._threads:
                thread.join()

            print('Completed. Goodbye!\n')
            exit(0)

    def _control(self, func_name, params, func):
        keys = set(params).intersection(self._controlValues.keys())
        kwNones = { k: ControlWrapper(None) for k in params }
        kwArgs = { k: self._controlValues[k] for k in keys }
        kwArgsWNones = { **kwNones, **kwArgs }
        with self._controlValuesLock:
            self._controlValues.update(kwArgsWNones)
        newthread = threading.Thread(target=func, kwargs=kwArgsWNones)
        newthread.daemon = True
        newthread.start()
        self._threads.append(newthread)





system = ControlSystemInterface()

def ControlThread(func):
    from inspect import signature
    parameters = signature(func).parameters.keys()
    system._control(func.__name__, parameters, func)
    return func

@ControlThread
def consoleThread():

    console = system.console
    prevLen = 0
    output = None
    buffered = None

    while system.active:
        if len(console._output) > 0:
            with console._outputLock:
                output, buffered = console._output.popleft()
            if prevLen > len(output):
                console._outputHandler.write(prevLen * ' ' + '\r')
                console._outputHandler.flush()
            if buffered:
                prevLen = len(output)
                output += '\r'
            console._outputHandler.write(output)
            console._outputHandler.flush()

