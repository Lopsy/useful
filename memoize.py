import collections
import functools
from hashify import hashify

class memoize(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
      self.hashifyON = False # whether we should call hashify on incoming data
   def __call__(self, *args):
      if not self.hashifyON:
         try:
            if args in self.cache:
               return self.cache[args]
         except TypeError:
            self.hashifyON = True
            # Replace the entire cache to avoid problems with submitting
            # [1,2] and then (list,1,2) as separate args to f
            newCache = {}
            # (Really stupid problem, but let's avoid the HORRIBLE case of
            # having to trace a bug back to this module)
            for key in self.cache:
               newCache[hashify(key)] = self.cache[key]
            self.cache = newCache
         value = self.func(*args)
         self.cache[args] = value
         return value
      # instead of not caching, we use hashify!!
      hashable = hashify(args)
      if hashable in self.cache:
         return self.cache[hashable]
      else:
         value = self.func(*args)
         self.cache[hashable] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)
