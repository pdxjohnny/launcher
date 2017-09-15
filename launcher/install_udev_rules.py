import os
import subprocess

GROUP = 'launcher'
RULES_FILE_NAME = '54-missilelauncher.rules'

class FailedToInstallRules(Exception): pass

def install_udev_rules(user, group=GROUP):
    '''
    Installs udev rules to allow non-root access to launchers.
    '''
    rule = 'SUBSYSTEM=="usb", ATTR{idVendor}=="2123", '
    rule += 'MODE="0660", GROUP="{}"\n'.format(group)
    dirs = ['/usr/lib/udev/rules.d/', '/etc/udev/rules.d/']
    for d in dirs:
        if os.path.isdir(d):
            with open(os.path.join(d, RULES_FILE_NAME), 'wb') as rules:
                rules.write(rule.encode('ascii'))
            with open(os.path.join(d, RULES_FILE_NAME), 'rb') as rules:
                if rules.read().decode() != rule:
                    raise FailedToInstallRules()
            subprocess.call(['udevadm', 'control', '--reload'])
            if user is not None:
                print('Adding {} to {} group...'.format(user, group))
                # subprocess.call(['udevadm', 'control', '--reload'])
                # print(os.getgrouplist(user))
            break
