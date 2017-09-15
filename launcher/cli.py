#!/usr/bin/python
import inspect
import argparse

import launcher

def nop(*args, **kwargs): return

def defaults(function):
    '''
    Returns the positional arguments for a fucntion and a dict of its
    keyword arguments with their defaults.
    '''
    args, varargs, keywords, defaults = inspect.getargspec(function)
    if args is None or defaults is None:
        return [], {}
    diff = len(args) - len(defaults)
    return args[:diff], dict(zip(args[diff:], defaults))

def function_to_parser(parser, function):
    args, kwargs = defaults(function)
    subparser = parser.add_parser(function.__name__.replace('_',
        '-'), help=function.__doc__)
    for k in args:
        subparser.add_argument(k, type=str)
    for k, v in kwargs.items():
        subparser.add_argument('--{}'.format(k), type=type(v),
                default=v)
    subparser.set_defaults(func=function)

def create_parser(functions=[], *args, **kwargs):
    parser = argparse.ArgumentParser(*args, **kwargs)
    subparsers = parser.add_subparsers()
    for func in functions:
        function_to_parser(subparsers, func)
    return parser

def main():
    parser = create_parser([
        launcher.install_udev_rules,
        launcher.control],
        prog='launcher',
        description=launcher.Launcher.__doc__)
    args = parser.parse_args()
    try:
        func = args.func
    except:
        return parser.parse_args(['-h'])
    kwargs = {i: getattr(args, i) for i in dir(args) \
            if not i.startswith('_') and not i == 'func'}
    args = [None for k, v in kwargs.items() if v == '']
    return func(*args, **kwargs)

if __name__ == '__main__':
    main()
