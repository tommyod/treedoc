#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:53:47 2019

@author: tommy
"""

import pydoc


def resolve_object(object_string):
    """
    Resolve a string to a Python object.
    
    
    list -> builtin
    collections -> module
    collections.Counter -> object
    
    Examples
    --------
    >>> resolve_object("list") == list
    True
    >>> import collections
    >>> resolve_object("collections") == collections
    True
    >>> from collections import Counter
    >>> resolve_object("collections.Counter") == Counter
    True
    >>> resolve_object("gibberish.Counter") is None
    True
    """
    assert isinstance(object_string, str)
    return pydoc.locate(object_string)


if __name__ == "__main__":
    import pytest

    # --durations=10  <- May be used to show potentially slow tests
    pytest.main(args=[".", "--doctest-modules", "-v", "--capture=sys"])
