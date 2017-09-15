import unittest

import launcher

class Testcmdstr(unittest.TestCase):

    def test_known(self):
        for i in range(6):
            self.assertNotEqual(launcher.cmdstr(1 << i), 'Unknown')

    def test_unknown(self):
        self.assertEqual(launcher.cmdstr(0xFF), 'Unknown')

class TestLauncherMethods(unittest.TestCase):

    def test_init(self):
        launcher.Launcher()

    def test_with(self):
        with launcher.TryLauncher()() as l:
            self.assertNotEqual(l.dev, False)

    def test_movement(self):
        with launcher.TryLauncher()() as l:
            l.up()
            l.down()
            l.left()
            l.right()

if __name__ == '__main__':
    unittest.main()
