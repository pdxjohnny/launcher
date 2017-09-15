from setuptools import find_packages, setup

with open('launcher/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

with open('README.rst', 'rb') as f:
    readme = f.read().decode('utf-8')

REQUIRES = ['pyusb']

setup(
    name='launcher',
    version=version,
    description='Controls Dream Cheeky USB Missile Launchers.',
    long_description=readme,
    author='John Andersen',
    author_email='johnandersenpdx@gmail.com',
    maintainer='John Andersen',
    maintainer_email='johnandersenpdx@gmail.com',
    url='https://github.com/pdxjohnny/launcher',
    license='Apache-2.0',

    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    install_requires=REQUIRES,
    tests_require=['coverage', 'pytest'],

    packages=find_packages(),

    entry_points={
        'console_scripts': (
            'launcher = launcher.cli:main',
        ),
    },
)
