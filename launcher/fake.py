import launcher

class FakeLauncher(launcher.Launcher):
    '''
    For when you don't have the USB launcher connected.
    '''

    def open(self):
        '''
        Does nothing instead of opening the USB device.
        '''
        return

    def cmd(self, cmd):
        '''
        Does nothing instead of sending USB commands to the launcher.
        '''
        return
