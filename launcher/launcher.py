# Copyright 2012, Nathan Milford
# Copyright 2017, John Andersen

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import time
from contextlib import contextmanager

import usb.core

class LauncherNotFound(Exception): pass
class OutOfAmmo(Exception): pass

UP = 0x02
DOWN = 0x01
LEFT = 0x04
RIGHT = 0x08
FIRE = 0x10
STOP = 0x20

def cmdstr(cmd):
    try:
        return {
                UP: 'up',
                DOWN: 'down',
                LEFT: 'left',
                RIGHT: 'right',
                FIRE: 'fire',
                STOP: 'stop'
                }[cmd]
    except: return 'Unknown'

class Launcher(object):
    '''
    Controls the Dream Cheeky Storm & Thunder USB Missile Launchers.
    Dream Cheeky is gone but here is the archive.org link.
    https://web.archive.org/web/20120209193259/http://www.dreamcheeky.com/
    '''
    num_shots = 4

    def __init__(self):
        self.dev = None
        self.shots = self.num_shots

    @contextmanager
    def __call__(self):
        '''
        A context manager to call open() and close().
        '''
        self.open()
        yield self
        self.close()

    def open(self):
        '''
        Opens the USB device.
        '''
        self.dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
        if self.dev is None:
            raise LauncherNotFound()
        if self.dev.is_kernel_driver_active(0) is True:
            self.dev.detach_kernel_driver(0)
        self.dev.set_configuration()
        return self

    def close(self):
        '''
        Closes the connection to the USB launcher device.
        '''
        self.cmd(0x20)
        return self

    def cmd(self, cmd):
        '''
        Sends a USB command to the launcher.
        '''
        return self.dev.ctrl_transfer(0x21, 0x09, 0, 0,
                [0x02, cmd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def stop(self):
        '''
        Stops the launcher from moving in that direction.
        '''
        time.sleep(0.1)
        return self.cmd(STOP)

    def up(self):
        '''
        Moves the launcher up.
        '''
        return self.cmd(UP) or self.stop()

    def down(self):
        '''
        Moves the launcher up.
        '''
        return self.cmd(DOWN) or self.stop()

    def left(self):
        '''
        Moves the launcher up.
        '''
        return self.cmd(LEFT) or self.stop()

    def right(self):
        '''
        Moves the launcher up.
        '''
        return self.cmd(RIGHT) or self.stop()

    def fire(self):
        '''
        Fires the missle in the the launcher.
        '''
        self.shots -= 1
        if self.shots <= 0:
            raise OutOfAmmo()
        return self.cmd(FIRE)

    def reload(self):
        '''
        Resets the shot count.
        '''
        self.shots = self.num_shots
        return self.shots
