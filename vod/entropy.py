# -*- coding: utf8
'''Module which contains functions to calculate entropy related metrics'''

from __future__ import division, print_function

import numpy as np
import numpy.ma as ma

def entropy(probabilities_x):
    '''
    Calculates the entropy (H) of the input vector which
    represents some random variable X.

    Parameters
    ----------
    probabilities_x: numpy array or any iterable
        Array with the individual probabilities_x. Values must be 0 <= x <=1
    '''
    probabilities_x = np.asanyarray(probabilities_x)
    
    assert (probabilities_x >= 0).all() and (probabilities_x <= 1).all()

    probabilities_x = probabilities_x[probabilities_x != 0]

    return -1 * (probabilities_x * np.log2(probabilities_x)).sum()

def mutual_information(probabilities_x, probabilities_xy):
    '''
    Calculates the mutual information between the
    random variables (X and X|Y):

    Parameters
    ----------
    probabilities_x: numpy array or any iterable
        Array with the individual probabilities X. Values must be 0 <= x <= 1

    probabilities_xy: numpy array or any iterable
        Array with the individual probabilities for X|Y. Values must be 0 <= x <= 1
    '''

    h_x = entropy(probabilities_x)
    h_xy = entropy(probabilities_xy)
    return h_x - h_xy

def norm_mutual_information(probabilities_x, probabilities_xy):
    '''
    Calculates the normalized mutual information between the
    random variables (X and X|Y):

    Parameters
    ----------
    probabilities_x: numpy array or any iterable
        Array with the individual probabilities X. Values must be 0 <= x <= 1

    probabilities_xy: numpy array or any iterable
        Array with the individual probabilities for X|Y. Values must be 0 <= x <= 1
    '''

    h_x = entropy(probabilities_x)
    h_xy = entropy(probabilities_xy)

    normalized_mi = 0
    if h_x > 0 and h_xy > 0:
        normalized_mi = 1 - (h_x - h_xy) / h_x
        
    return normalized_mi

def kullback_leiber_divergence(probabilities_p, probabilities_q):
    '''
    Calculates the Kullback-Leiber divergence between the distributions
    of two random variables.

    $$ D_{kl}(P(X) || Q(X)) = \sum_{x \in X) p(x) * log(\frac{p(x)}{q(x)}) $$

    Parameters
    ----------
    probabilities_p: numpy array or any iterable
        Array with the individual probabilities P. Values must be 0 <= x <= 1

    probabilities_q: numpy array or any iterable
        Array with the individual probabilities for Q. Values must be 0 <= x <= 1
    '''
    probabilities_p = np.asanyarray(probabilities_p)
    probabilities_q = np.asanyarray(probabilities_q)

    assert (probabilities_p >= 0).all() and (probabilities_p <= 1).all()
    assert (probabilities_q >= 0).all() and (probabilities_q <= 1).all()
    
    non_zero_p = probabilities_p != 0
    non_zero_q = probabilities_q != 0
    
    #n * log(n / 0) = inf (definition of kullback leiber)
    #by subtracting boolean arrays, we need an zero array for equality
    if (non_zero_p - non_zero_q).any():
        return np.inf
    
    #from here we know that non_zero_x == non_zero_y
    probabilities_p = probabilities_p[non_zero_p != 0]
    probabilities_q = probabilities_q[non_zero_q != 0]

    log_part = np.log2(probabilities_p) - np.log2(probabilities_q)
    return (probabilities_p * log_part).sum()
