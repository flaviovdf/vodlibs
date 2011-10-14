# -*- coding: utf8
'''
Tests for the go module. All values
here were pre-computed by hand or extracted from book
examples.
'''
from __future__ import division, print_function

from vod.stats.gof import chisq_poisson

import random
import unittest

class TestGOF(unittest.TestCase):

    def test_example_one(self):
        '''
        Based on the example:
        http://goo.gl/PO0U8
        (we do not treat minimum frequencies as the authors does)
        '''
        data = [8] * 2 + [7] * 5 + [6] * 10 + [5] * 21 + \
               [4] * 29 + [3] * 41 + [2] * 47 + [1] * 31 + [0] * 14
        
        random.shuffle(data)
        
        result = chisq_poisson(data)
        self.assertAlmostEqual(2.28, result[0], 2)
        self.assertAlmostEqual(0.94, result[1], 2)
        
    def test_example_two(self):
        '''
        Based on the example:
        http://mlsc.lboro.ac.uk/resources/statistics/gofit.pdf
        (we do not treat minimum frequencies as the authors does)
        '''
        
        data = [3] * 4 + [2] * 9 + [1] * 15 + [0] * 32
        
        random.shuffle(data)
        result = chisq_poisson(data)
        self.assertAlmostEqual(3.46, result[0], 2)
        self.assertAlmostEqual(0.18, result[1], 2)
        
    def test_example_three(self):
        '''Same as one but with non contiguous data'''
        data = [9] * 2 +  [7] * 5 + [6] * 10 + [5] * 21 + \
               [4] * 29 + [3] * 41 + [2] * 47 + [1] * 31 + [0] * 14
        
        random.shuffle(data)
        
        result = chisq_poisson(data)
        self.assertAlmostEqual(6.69, result[0], 2)
        self.assertAlmostEqual(0.57, result[1], 2)

if __name__ == "__main__":
    unittest.main()