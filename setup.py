#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import division, print_function
'''Setup script'''

import glob
import os
import sys

from distutils.core import setup

SOURCE = 'src/'
os.chdir(SOURCE)

if sys.version_info[:2] < (2, 7):
    print('Requires Python version 2.7 or later (%d.%d detected).' %
          sys.version_info[:2])
    sys.exit(-1)

def get_packages():
    '''Appends all packages (based on recursive sub dirs)'''

    packages  = ['vod']

    for package in packages:
        base = os.path.join(package, '**/')
        sub_dirs = glob.glob(base)
        while len(sub_dirs) != 0:
            for sub_dir in sub_dirs:
                package_name = sub_dir.replace('/', '.')
                if package_name.endswith('.'):
                    package_name = package_name[:-1]

                packages.append(package_name)
        
            base = os.path.join(base, '**/')
            sub_dirs = glob.glob(base)

    return packages

if __name__ == "__main__":
    packages = get_packages()
    
    setup(name             = 'vodlibs',
            packages         = packages)
