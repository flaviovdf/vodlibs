# -*- coding: utf8
'''
Tests for the corr module
'''
from __future__ import division, print_function

from vod.stats.corr import dcorr

import numpy as np
import random
import unittest

class TestCorr(unittest.TestCase):

    def test_hyperbole(self):
        np.random.seed(9854673)
        x = np.linspace(-1,1, 501)
        y = - x**2 + 0.2 * np.random.rand(len(x))

        self.assertAlmostEqual(0.48012498, dcorr(x, y), 4)

    def test_circle(self):
        np.random.seed(9854673)
        x = np.linspace(-1,1, 501)
        y = np.cos(x*2*np.pi) + 0.1 * np.random.rand(len(x))

        self.assertAlmostEqual(0.24919872, dcorr(x, y), 4)

if __name__ == "__main__":
    unittest.main()
