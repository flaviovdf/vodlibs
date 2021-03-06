# -*- coding: utf8
'''
Tests for the confidence interval module. All values
here were pre-computed by hand or extracted from book
examples.
'''

from __future__ import division, print_function

from vod.stats.ci import half_confidence_interval_size
from vod.stats.ci import min_sample_size

from numpy.testing import *

import unittest
from numpy.ma.testutils import assert_array_almost_equal

class TestCI(unittest.TestCase):

    def test_min_sample_size(self):
        data = [40.0, 0.0, 40.0, 0.0]
        self.assertAlmostEqual(4051.185794406982, 
                               min_sample_size(data, 0.95, 0.05))
        
        data = [8.0, 7.0, 5.0, 9.0, 9.5, 11.3, 5.2, 8.5, 4.0, 7.4, 4.4, 
                9.0, 1.1, 0.0, 0.2, 9.5, 1.0, 2.0, 3.0, 4.0, 5.5, 8.2, 
                4.2, 4.5, 7.2, 7.0, 1.2, 5.3, 8.5, 1.3, 5.3, 9.5]
        self.assertAlmostEqual(21060.339060549919, 
                               min_sample_size(data, 0.99, 0.01))

    def test_min_sample_size_axis(self):
        data = [[40.0, 0.0, 40.0, 0.0], 
               [40.0, 0.0, 40.0, 0.0]]
         
        self.assertAlmostEqual(2236.5791393864079, 
                               min_sample_size(data, 0.95, 0.05))
        
        x = 4051.185794406982
        assert_array_almost_equal([x, x],
                                  min_sample_size(data, .95, .05, 1))
        
    def test_confidence_interval(self):
        data = [8.0, 7.0, 5.0, 9.0, 9.5, 11.3, 5.2, 8.5]
        
        self.assertAlmostEqual(1.6772263663789651, 
                               half_confidence_interval_size(data, 0.95), 5)
    
    
        data = [8.0, 7.0, 5.0, 9.0, 9.5, 11.3, 5.2, 8.5, 
                4.0, 7.4, 4.4, 9.0, 1.1, 0.0, 0.2, 9.5, 
                1.0, 2.0, 3.0, 4.0, 5.5, 8.2, 4.2, 4.5, 
                7.2, 7.0, 1.2, 5.3, 8.5, 1.3, 5.3, 9.5]
        self.assertAlmostEqual(1.4173919794304153, 
                               half_confidence_interval_size(data, 0.99), 5)

    def test_confidence_interval_axis(self):
        data = [[8.0, 7.0, 5.0, 9.0, 9.5, 11.3, 5.2, 8.5],
                [8.0, 7.0, 5.0, 9.0, 9.5, 11.3, 5.2, 8.5]]

        assert_array_almost_equal([1.67722628,  1.67722628],
                                  half_confidence_interval_size(data, .95, 
                                                                axis=1))

        assert_array_almost_equal([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                                  half_confidence_interval_size(data, .95, 
                                                                axis=0))
        
        self.assertAlmostEqual(1.06902922476,
                               half_confidence_interval_size(data, .95))
        
if __name__ == "__main__":
    unittest.main()