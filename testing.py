# -*- coding: utf-8 -*-

"""Main module."""

def recurse_on(obj):
    return inspect.ismodule(obj) or inspect.isclass(obj)

def is_method(obj):
    return inspect.ismethoddescriptor(obj) or inspect.ismethod(obj)

def is_interesting(obj):
    
    funcs = [getattr(inspect, method) for method in dir(inspect) if 'is' ==  method[:2]]
    
    return any([func(obj) for func in funcs])

import inspect

from collections.abc import Callable
import time

def yield_data(obj, stack=None):
    time.sleep(0.1)
    
    print(f"yield_data({obj}, stack={stack})")
    
    if stack is None:
        stack = []
    stack += [obj]  
    
    yield stack
    
    for (name, attribute) in inspect.getmembers(obj):
        
        if name in ('__class__', '__doc__', '__hash__'):
            continue
        
        if not is_interesting(attribute):
            continue
        
        
        if not recurse_on(attribute):
            yield stack + [attribute]
        else:
            yield from yield_data(attribute, stack=stack)
        
import math
import os
import collections
for builtin in [int, tuple, list, dict, time, math]:
 
        
    for row in yield_data(builtin):
        print(*[c for c in row], sep="->")
        print(*[c.__name__ for c in row], sep="->")
        print()
    
for row in yield_data(math):
    print(*[c.__name__ for c in row], sep="->")