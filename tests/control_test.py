import unittest
import multiprocessing

import launcher

class TestControlLauncherMethods(unittest.TestCase):

    def test_getc(self):
        r, w = multiprocessing.Pipe()
        w.send('A')
        self.assertEqual(launcher.ControlLauncher().getc(fd=r), 'A')

    def test_movement(self):
        r, w = multiprocessing.Pipe()
        w.send('A')
        w.send('W')
        w.send('S')
        w.send('D')
        w.send(' ')
        w.send(' ')
        w.send(' ')
        w.send(' ')
        w.send(' ')
        w.send('R')
        w.close()
        launcher.control(fd=r)

if __name__ == '__main__':
    unittest.main()
