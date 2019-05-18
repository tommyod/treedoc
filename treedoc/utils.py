#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General utilities for treedoc.
"""

import collections

class PrintMixin:
    """Adds a __repr__ method to a class."""

    # Could've used dataclasses, but they were introduced in Python 3.8

    def __repr__(self):
        """Returns a string like ClassName(a=2, b=3)."""
        args = ["{}={}".format(k, v) for k, v in self.__dict__.items()]
        return type(self).__name__ + "({})".format(", ".join(args))


_marker = object()


class Peekable:
    """Wrap an iterator to allow lookahead.
    
    Call `peek` on the result to get the value that will be returned by `next`. 
    This won't advance the iterator:
        
    >>> p = Peekable(['a', 'b'])
    >>> p.peek()
    'a'
    >>> next(p)
    'a'
        
    Pass `peek` a default value to return that instead of raising ``StopIteration`` 
    when the iterator is exhausted.
    
    >>> p = Peekable([])
    >>> p.peek('hi')
    'hi'

    """

    def __init__(self, iterable):
        self._it = iter(iterable)
        self._cache = collections.deque()

    def __iter__(self):
        return self

    def __bool__(self):
        try:
            self.peek()
        except StopIteration:
            return False
        return True

    def peek(self, default=_marker):
        """Return the item that will be next returned from ``next()``.
        
        Return ``default`` if there are no items left. If ``default`` is not
        provided, raise ``StopIteration``.
        """
        if not self._cache:
            try:
                self._cache.append(next(self._it))
            except StopIteration:
                if default is _marker:
                    raise
                return default
        return self._cache[0]

    def __next__(self):
        if self._cache:
            return self._cache.popleft()

        return next(self._it)
