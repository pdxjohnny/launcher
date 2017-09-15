import os
import sys
import fcntl
import termios
import multiprocessing

import launcher.trylauncher

def control(fd=None):
    ControlLauncher.control(fd=fd)

class ControlLauncher(launcher.trylauncher.TryLauncher):
    '''
    Echo commands and controlable with AWSD keys.
    '''

    def cmd(self, cmd):
        '''
        Echos commands.
        '''
        super().cmd(cmd)
        if self.isopen:
            return
        print(launcher.cmdstr(cmd))

    @staticmethod
    def getc(fd=None):
        '''
        Get a single character from the UNIX command line.
        '''
        if fd == None: fd = sys.stdin

        read = getattr(fd, 'recv', getattr(fd, 'read', None))
        try:
            oldterm = termios.tcgetattr(fd.fileno())
            newattr = termios.tcgetattr(fd.fileno())
            newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(fd.fileno(), termios.TCSANOW, newattr)

            oldflags = fcntl.fcntl(fd.fileno(), fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
        except: pass

        try:
            while 1:
                try:
                    print(fd.__class__.__name__.lower())
                    if fd.__class__.__name__.lower() == 'connection':
                        c = read()
                    else: c = read(1)
                    break
                except IOError: pass
        finally:
            try:
                termios.tcsetattr(fd.fileno(), termios.TCSAFLUSH,
                        oldterm)
                fcntl.fcntl(fd.fileno(), fcntl.F_SETFL, oldflags)
            except: pass
        return c

    @classmethod
    def control(cls, fd=None):
        '''
        Control the USB connected launcher or echos commands if not.
        '''
        self = cls()
        self.open()
        try:
            while True:
                x = self.getc(fd=fd).lower()
                if x == 'w':
                    self.up()
                elif x == 'a':
                    self.left()
                elif x == 's':
                    self.down()
                elif x == 'd':
                    self.right()
                elif x == 'r':
                    self.reload()
                    print('Reloaded', self.shots)
                elif x == ' ':
                    try:
                        self.fire()
                        print('Fire!', self.shots, 'left')
                    except launcher.launcher.OutOfAmmo:
                        print('Reload!')
                # termios.tcflush(sys.stdin, termios.TCIOFLUSH)
        except KeyboardInterrupt: pass
        except EOFError: pass
        self.close()
