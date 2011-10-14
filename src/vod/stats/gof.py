# -*- coding: utf8
'''
Some custom goodness of fit tests
'''
from __future__ import division, print_function

from scipy import stats

import numpy as np

def chisq_poisson(data):
    '''
    Tests if the data comes from a Poisson distribution. This is done using
    the Pearson Chi-Square test. Each value from the data given is treated like
    a categorical attribute, where the number of occurrences of the value is
    tested against the expected occurrences if the data came from a Poisson
    distribution. The hypothesis are:
        
        * H0 (null) - The data comes from a poisson distribution
        * H1 - The data does NOT comes from a poisson distribution
    
    Arguments
    ---------
    data: array like
        Array with observations
    
    Returns
    -------
    (chi-square value, p-value): The chi-square value found and a p-value
                                 for the null hypothesis.
    
    Notes
    -----
    This implementation does not do any special treatment for values with
    small number of occurrences. If this is an issue, we recommend you
    compute expected frequencies and use the Scipy `stats.chisquare`.
    '''
    observed = np.asanyarray(data)
    
    #All possible frequencies from [min(observed) to max(observed)]
    #Those who are not in observed, have frequency = 0. The frequency
    #of a value is is accessed by all_freq[value].
    all_freqs = np.bincount(observed)
    all_values = np.arange(len(all_freqs))
    
    #Estimating the mean of the Poisson
    aux = (all_freqs * all_values).sum()
    total = all_freqs.sum()
    estimated_mean = aux / total

    #Computes expected frequencies in ascending order of the values
    #First for all values till the one before the last
    dist = stats.poisson(estimated_mean)
    probabilites = np.apply_along_axis(dist.pmf, 0, all_values[:-1])
    last_value = all_values[-1]
    
    #Add greater or equal last one
    geq_last = dist.sf(last_value) + dist.pmf(last_value)
    probabilites = np.append(probabilites, geq_last)
    expected_freqs = total * probabilites
    
    #Now the arrays are matched (each index is the frequency of the same value)
    chisq = stats.chisquare(all_freqs, expected_freqs)[0]
    pval = stats.chisqprob(chisq, len(all_freqs) - 2)
    return chisq, pval