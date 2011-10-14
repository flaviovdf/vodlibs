# -*- coding: utf8

from __future__ import division, print_function

import numpy as np

def least_square(xpts, ypts):
    '''
    Performs a basic least square regression for a curve:
        
        y = ax + b
    
    Returns estimated (a, b), residuals array and totals
    arrays. We need this method because numpy's polyfit
    does not return the residuals and totals arrays, only
    their sums.
    '''
    assert len(xpts) == len(ypts)
    
    n_points = len(xpts)
    sum_x  = np.add.reduce(xpts)
    sum_y  = np.add.reduce(ypts)
    sum_xy = np.add.reduce(xpts * ypts)
    sum_xx = np.add.reduce(xpts**2)

    a = (n_points * sum_xy - sum_x * sum_y) / (n_points * sum_xx - sum_x ** 2)
    b = (sum_y - a * sum_x) / n_points

    func = lambda point: b + a*point
    estimated = np.apply_along_axis(func, 0, xpts)
    residuals = estimated - ypts
    totals = ypts - np.mean(ypts)
    
    return (a, b), residuals, totals

def least_square_powerlaw(xpts, ypts):
    """
    Fits a powerlaw using the log transformation.
    """
    
    log_x = np.log10(xpts)
    log_y = np.log10(ypts)

    return least_square(log_x, log_y)