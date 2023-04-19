#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' __init__.py used to mark directories as Python package directories '''

__description__ = 'task: __init__'
__version__ = '1.0.1'
__author__ = 'Stephan Metzler'
__email__ = 'metl@zhaw.ch'
__status__ = 'build your way to extraordinary'

'''
__init__.py     used to mark directories as Python package directories

__all__         is a list of strings defining what symbols in a module will
                be exported when from <module> import * is used on the module.
                __all__ affects the from <module> import * behavior only.
                Members that are not mentioned in __all__ are still accessible
                from outside the module and can be imported with
                from <module> import <member>.
e.g.:

__all__ = [
    'Task',
    'DynamicEconomy',
    'FireBlaze',
    'GrowingPopulation',
    'MovingCar',
    'PublicSafty',
    'VirusCondanimation'
    ]

'''

import os

# build __all__ dynamically from all classes in directory
path = os.path.dirname(os.path.abspath(__file__))
__all__ = [cls for cls in [f[:-3]
    for f in os.listdir(path)
    if f.endswith('.py') and f != '__init__.py']]


if __name__ == '__main__':  # to test
    for task in __all__:
        print(task)
