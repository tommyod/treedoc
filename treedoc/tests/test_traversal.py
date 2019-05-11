#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:38:59 2019

@author: tommy
"""

from treedoc.traversal import ObjectTraverser

import treedoctestpackage as testpackage
import treedoctestpackage.subpackage as subtestpackage


def test_traversal():
    assert True


def test_recusions():

    traverser = ObjectTraverser(subpackages=True)
    assert traverser.recurse_to_child_object(testpackage, subtestpackage)

    traverser = ObjectTraverser(subpackages=False)
    assert not traverser.recurse_to_child_object(testpackage, subtestpackage)


if __name__ == "__main__":
    import pytest

    pytest.main(args=[".", "--doctest-modules", "-v", "--capture=sys"])
