import launcher

class TryLauncher(launcher.Launcher):
    '''
    For when you don't know if you have the USB launcher connected.
    '''

    def open(self):
        '''
        If super().open() fails we set isopen to False.
        '''
        self.isopen = True
        try:
            super().open()
        except:
            self.isopen = False

    def cmd(self, cmd):
        '''
        Sends commands if isopen is True.
        '''
        if self.isopen:
            return super().cmd(cmd)
