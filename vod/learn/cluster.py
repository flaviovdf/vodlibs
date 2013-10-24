# -*- coding: utf8
'''
Common code for clustering tasks
'''
from __future__ import division, print_function

from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import pairwise

from vod.stats.ci import half_confidence_interval_size

import numpy as np

def kmeans_betacv(data, num_cluster, batch_kmeans=False, n_runs = 10,
                  confidence = 0.90):
    '''
    Computes the BetaCV for running Kmeans on the dataset. This method
    returns the BetaCV value and half of the size of the confidence interval
    for the same value (BetaCV is an average or the number of runs given).
    
    Arguments
    ---------
    data: matrix
        A matrix of observations. If this is sparse, `batch_kmeans` must 
        be True
    num_cluster: int 
        number of clusters to run k-means for
    batch_kmeans: bool (defauts to False)
        if `sklearn.cluster.MiniBatchKMeans` should be used. This is faster
        and suitable for sparse datasets, but less accurate.
    n_runs: int (default = 10)
        Number of runs to compute the BetaCV
    confidence: double [0, 1) (default = 0.9)
        The confidence used to compute half the confidence interval size
    
    Returns
    -------
    The betacv and half of the confidence interval size
    '''
    algorithm = None
    if not batch_kmeans:
        algorithm = KMeans(num_cluster)
    else:
        algorithm = MiniBatchKMeans(num_cluster)
    
    inter_array = np.zeros(n_runs)
    intra_array = np.zeros(n_runs)
    for i in xrange(n_runs):
        #Run K-Means
        algorithm.fit(data)
        
        centers = algorithm.cluster_centers_
        labels = algorithm.labels_
        
        #KMeans in sklearn uses euclidean
        dist_centers = pairwise.euclidean_distances(centers)
        
        #Inter distance
        mean_dist_between_centers = np.mean(dist_centers)
        inter_array[i] = mean_dist_between_centers

        #Intra distance
        dist_all_centers = algorithm.transform(data)
        intra_dists = []
        for doc_id, cluster in enumerate(labels):
            dist = dist_all_centers[doc_id, cluster]
            intra_dists.append(dist)
        intra_array[i] = np.mean(intra_dists)
    
    betacv = intra_array / inter_array
    cinterval = half_confidence_interval_size(betacv, confidence)
    return np.mean(betacv), cinterval