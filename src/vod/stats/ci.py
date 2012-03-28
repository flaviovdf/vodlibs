# -*- coding: utf-8
'''Confidence interval related code'''

from __future__ import division, print_function

from scipy.stats import t, norm

import math
import numpy as np

def min_sample_size(data, confidence, err, axis=None):
    """
    Determines the minimum (expected) sample size needed to have the confidence
    interval (mean(data) +- err*mean(data)).
    
    >>> data = [40.0, 0.0, 40.0, 0.0]
    >>> min_sample_size(data, 0.95, 0.05)
    4051.185794406982
    """
    
    a = np.asanyarray(data)
    
    if axis is None:
        n = a.size
    else:
        n = a.shape[axis]
        
    mean = np.mean(a, axis=axis) 
    std = np.std(a, axis=axis)
    
    if n <= 30:
        c = t_table(n - 1, confidence)
    else:
        c = z_table(confidence)
        
    n = ( (std * c) / (err * mean) )**2
    return n
    
def half_confidence_interval_size(data, confidence, axis=None):
    """
    Determines the half of the confidence interval size
    for some data. The confidence interval is mean +- return values.
    
    >>> data = [8.0, 7.0, 5.0, 9.0, 9.5, 11.3, 5.2, 8.5]
    >>> confidence_interval(data, 0.95)
    1.6772263663789651
    """
    
    a = np.asanyarray(data)
    if axis is None:
        n = a.size
    else:
        n = a.shape[axis]
        
    std = np.std(a, axis=axis)
    
    # calls the inverse CDF of the Student's t
    # distribution
    if n <= 30:
        h = std * t_table(n-1, confidence) / math.sqrt(n)
    else:
        h = std * z_table(confidence) / math.sqrt(n)
    return h

def t_table(freedom, confidence):
    """
    Looks up the t_table (i.e. calls the inverse CDF of the 
    t-student distribution).
    
    >>> t_table(1, 0.95)
    12.706204736432099
    >>> t_table(9, 0.90)
    1.8331129326536333
    >>> t_table(8, 0.99)
    3.3553873313333957
    >>> t_table(10, 0.85)
    1.5592359332425447
    """
    return t.ppf((1+confidence)/2.,freedom)

def z_table(confidence):
    """
    Looks up the z_table (i.e. calls the inverse CDF of the 
    normal distribution).
    
    >>> z_table(0.95)
    1.959963984540054
    >>> z_table(0.90)
    1.6448536269514722
    >>> z_table(0.99)
    2.5758293035489004
    >>> z_table(0.85)
    1.4395314709384561
    """
    return norm.ppf((1+confidence)/2.)