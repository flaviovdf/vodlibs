# -*- coding: utf8
'''
Tests for the fit module. All values
here were pre-computed by hand or extracted from book
examples.
'''
from __future__ import division, print_function

from vod.stats.fit import least_square_powerlaw

import numpy as np
import unittest

class TestFIT(unittest.TestCase):

    def test_powerlaw(self):
        x = [0.125, 0.325, 0.525, 0.725, 0.825]
        y = [2.420, 3.760, 4.750, 5.520, 5.870]

        result = least_square_powerlaw(x, y)
        expected = np.polyfit(np.log10(x), np.log10(y), 1, full=True)
        self.assertAlmostEqual(expected[0][0], result[0][0])
        self.assertAlmostEqual(expected[0][1], result[0][1])
        self.assertAlmostEqual(expected[1][0], (result[1] ** 2).sum())
        
if __name__ == "__main__":
    unittest.main()