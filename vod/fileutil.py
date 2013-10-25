# -*- coding: utf8
'''
Functions for writing data to file.
'''
from __future__ import division, print_function

import numpy as np

def write_xy_to_file(x_vals, y_vals, fpath):
    '''
    Writes two equal length arrays as columns in a text file.
    
    Arguments
    ---------
    x_vals: array like
        the values for the first column
    y_vals: array like
        the values for the second column
    fpath: str
        The path of the file to write to
    '''
    assert 'Not same length', len(x_vals) == len(y_vals)
    with open(fpath, 'w') as data_file:
        for i in xrange(len(x_vals)):
            print(x_vals[i], y_vals[i], file=data_file) 

def write_col_to_file(data, fpath):
    '''
    Writes an array as a column in a text file.
    
    Arguments
    ---------
    data: array like
        the values for the column
    fpath: str
        The path of the file to write to
    '''
    
    with open(fpath, 'w') as data_file:
        for i in xrange(len(data)):
            print(data[i], file=data_file) 

def write_stats_to_file(data, fpath):
    '''
    Writes some basic stats about and array and
    also the array as a column in a text file.
    
    Arguments
    ---------
    data: array like
        the values for the column
    fpath: str
        The path of the file to write to
    '''
    
    with open(fpath, 'w') as data_file:
        print('#n ', len(data), file=data_file)
        print('#mean ', np.mean(data), file=data_file)
        print('#median ', np.median(data), file=data_file)
        print('#std ', np.std(data), file=data_file)
        for i in xrange(len(data)):
            print(data[i], file=data_file)