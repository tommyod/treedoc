#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 21:03:07 2019

@author: tommy
"""

import inspect
import sys


def simpleprint(row, stream=sys.stdout, hide_magic=True):

    # try:
    # doc = inspect.getdoc(row[-1])
    
    *_, last = row
    #print(last)
    
    if last.__name__.endswith('__') and last.__name__.startswith('__'):
        if hide_magic:
            return


    print(*[c.__name__ for c in row], sep="->", file=sys.stdout, end="\n")
    try:
        pass
        # print(inspect.signature(row[-1])[:50], file=sys.stdout)
    except (TypeError, ValueError):
        pass
