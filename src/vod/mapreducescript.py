# -*- coding: utf-8
'''
Simple module which creates a pool of processes to work
on items retrieved by an iterator.
'''
from __future__ import division, print_function

from abc import abstractmethod
from abc import ABCMeta
from multiprocessing import Pool

import argparse
import cProfile as profile
import pstats
import sys
import traceback

class BaseMapper(object):
    '''This class can be used to
       safely create Mappers'''

    __metaclass__ = ABCMeta
    
    @abstractmethod
    def _map(self, key, item):
        '''
        This method is wrapped by the __call__
        method. It should perform some operations
        on the item and return the tuple: value.
        The value represents the result of the operation.
        '''
        pass
    
    def __call__(self, key, item):
        return self._map(key, item)

class Runner(object):
    '''
    This class can be used to create programs which work
    in a simple map-reduce manner. The master creates slaves
    to apply map functions to an iterator, it will then reduce
    the results of this function.
    
    Runners are a simple framework for creating map-reduce like
    scripts. They make use of the `argparse` module for configuration.
    By default, each runner has the following arguments:
       * num_procs : The number of processes to use
       * --profile (optional) : If execution should be profiled
    Other arguments are defined by inheritance.
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    @abstractmethod
    def item_generator(self):
        '''
        Implementations of this method must return either
        a generator or a iterator which yields a tuple: 
        (key, item)
        '''
        pass
    
    @abstractmethod
    def mapper(self):
        '''
        Must return a `Callable` which
        can receive as parameters a key and an item.
        
        For example:
        mapper = self.mapper()
        value = mapper(key, someobject)
        
        Due to the fact the functions cannot be pickled (serialized),
        this class does not work with lambdas or class methods.

        The safest way to create a reducer is to inherit
        `BaseMapper`
        '''
        pass
    
    @abstractmethod
    def reducer(self):
        '''
        Must return a `Callable` which
        can receive as parameters a key and an value.
        
        The value is the result of processing some item
        with the processor. 

        proc = self.processor()
        value = proc(key, someobject)
        reduc = self.reducer()
        reduc(key, value)
        '''
        pass
    
    def add_custom_aguments(self, parser):
        '''
        Inherit this method to add custom arguments to
        the argument parser.
        
        This method will be called before anything is run, so
        you can add your new argumente. For example:
        
        parser.add_argument('in_dir',  type=str, 
                            help='The directory with input files')
        
        The code runs as follows:
        1. creates a argparse with default arguments
        2. adds custom arguments with the `add_custom_aguments`
           method
        3. Passes the command line arguments (or any array) to
           the parser
        4. Calls `setup`
        '''
        pass

    def setup(self, arg_vals):
        '''
        Inherit this method to make use of arguments
        passed in the command line. 
        
        This method is called after the `add_custom_aguments`.
        You should use it to extract the argumets the user
        supplied in the command line. For example:
        
        self.in_dir = arg_vals.in_dir
        
        The code runs as follows:
        1. creates a argparse with default arguments
        2. adds custom arguments with the `add_custom_aguments`
           method
        3. Passes the command line arguments (or any array) to
           the parser
        4. Calls `setup`
        '''
        pass

    def __call__(self, args = None):
        if not args: 
            args = []
        
        parser = argparse.ArgumentParser(prog=self.name,
                                         description=self.description)
        try:
            parser.add_argument('num_procs',  type=int, 
                                help='Number or parallel processors')
            parser.add_argument('--profile',  action='store_true', 
                                help='Profile the execution?')
                        
            self.add_custom_aguments(parser)
            arg_vals = parser.parse_args(args)
            self.setup(arg_vals)
            
            num_procs = arg_vals.num_procs
            if arg_vals.profile: #will profile and summarize using pstats
                print('saving profiler output to: .run_profile.prof',
                      file = sys.stderr)
                
                profile.runctx('self._go(num_procs)', 
                               globals(), locals(), '.run_profile.prof')
                
                stats = pstats.Stats('.run_profile.prof').\
                        strip_dirs().sort_stats('time')
                stats.print_stats()
            else: #normal execution
                self._go(num_procs)
                
        except Exception:
            parser.print_help(file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
    
    def _go(self, num_procs):
        '''
        This is the equivalent of the main method. It will 
        create the processes and the pipeline between item generators -> 
        mappers -> a reducer.
        '''
        pool = None
        try:
            print('Initiating...', file=sys.stderr)
    
            igen = self.item_generator()
            reducer = self.reducer()
            mapper = self.mapper()
            
            if (num_procs > 1):
                print('Using %d processes' %num_procs, file=sys.stderr)
                
                def igen_helper():
                    '''
                    Helper generator to pass the mapper object
                    to each slave process
                    '''
                    for key, item in igen:
                        yield (mapper, key, item)
                
                pool = Pool(num_procs)
                results = pool.imap(_processor_helper, 
                                    igen_helper(), 100)
                
                for key, value in results:
                    reducer(key, value)
    
            else:
                print('Using one mapper only', file = sys.stderr)
                    
                for key, item in igen:
                    value = mapper(key, item)
                    reducer(key, value)
            
            print('Done.', file = sys.stderr)
        finally:
            if pool:
                pool.close()
                pool.join()

def _processor_helper(tup):
    '''Helper for the use of multiprocessing'''
    processor, key, item = tup
    return key, processor(key, item)