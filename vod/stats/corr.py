#-*- coding: utf8
from __future__ import division, print_function
'''
Contains more uncommon correlation measures. Currently, 
distance correlation only
'''

from scipy.spatial.distance import cdist

import numpy as np

def _get_distance_matrix(X):

    #None indexing adds a new dimension
    #[1][:, None] -> [[1]]
    if X.ndim == 1:
        X = X[:, None]
    
    if X.ndim != 2:
        raise Exception('1d or 2d arrays expected as input')

    return cdist(X, X, 'euclidean')

def _dcov_from_matrices(Dx, Dy):
    
    A = Dx.copy()
    B = Dy.copy()

    #grand means
    gm_a = A.mean()
    gm_b = B.mean()

    #row means
    row_a = A.mean(axis=0)
    row_b = B.mean(axis=0)
    
    #col means
    col_a = A.mean(axis=1)[:, None]
    col_b = B.mean(axis=1)[:, None]
    
    #using None as trick to perform operation on column axis
    A = A - row_a - col_a + gm_a
    B = B - row_b - col_b + gm_b
    
    return (A * B).mean()

def dcov(X, Y):
   
    X = np.asanyarray(X)
    Y = np.asanyarray(Y)

    if X.shape[0] != Y.shape[0]:
        raise Exception('X and Y must have same number of rows')

    Dx = _get_distance_matrix(X)
    Dy = _get_distance_matrix(Y)
    
    return _dcov_from_matrices(Dx, Dy)
    
def dcorr(X, Y):

    X = np.asanyarray(X)
    Y = np.asanyarray(Y)

    if X.shape[0] != Y.shape[0]:
        raise Exception('X and Y must have same number of rows')

    Dx = _get_distance_matrix(X)
    Dy = _get_distance_matrix(Y)

    dvar_x = _dcov_from_matrices(Dx, Dx)
    dvar_y = _dcov_from_matrices(Dy, Dy)
    dcov_xy = _dcov_from_matrices(Dx, Dy)
    
    return np.sqrt(dcov_xy / np.sqrt((dvar_x * dvar_y)))
