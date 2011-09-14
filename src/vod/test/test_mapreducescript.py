# -*- coding: utf8
'''Tests for the map-reduce module'''

from __future__ import division, print_function

from vod.mapreducescript import BaseMapper
from vod.mapreducescript import Runner 

import unittest

class RunnerTest(unittest.TestCase):
    '''Tests the Runner class'''
    
    def testAll(self):
        r1 = BasicRunner()
        r1(['100'])
        self.assertEquals(100, len(r1.result_store))
        
        for k, v in r1.result_store.items():
            self.assertEquals(k, v - 1)
            
        r2 = BasicRunner()
        r2(['1'])
        self.assertEquals(100, len(r2.result_store))
            
        for k, v in r2.result_store.items():
            self.assertEquals(k, v - 1)
                    
        self.assertEquals(r1.result_store, r2.result_store)

class Processor(BaseMapper):
    
    def _map(self, key, item):
        return item + 1
    
class BasicRunner(Runner):
    
    def __init__(self):
        super(BasicRunner, self).__init__('Basic', 'Blah')
        self.igen = ((i, i) for i in xrange(100))
        self.result_store = {}
        
        self.proc = Processor()
        
        def _reduc(key, value): 
            self.result_store[key] = value   
        self.reduc = _reduc 
    
    def item_generator(self):
        return self.igen
    
    def mapper(self):
        return self.proc 
    
    def reducer(self):
        return self.reduc