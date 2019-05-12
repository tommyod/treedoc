#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:38:59 2019

@author: tommy
"""

import itertools
import operator

import pytest
import inspect
import treedoctestpackage as testpackage
import treedoctestpackage.subpackage as subtestpackage
from treedoc.traversal import ObjectTraverser
from treedoctestpackage import module


def test_traversal():
    assert True


@pytest.mark.parametrize("modules", [True, False])
def test_recusion_subpackages(modules):
    """Regardless of what the `modules` flag says, the following should hold."""

    traverser = ObjectTraverser(subpackages=True, modules=modules)
    assert traverser.recurse_to_child_object(obj=testpackage, child_obj=subtestpackage)

    traverser = ObjectTraverser(subpackages=False, modules=modules)
    assert not traverser.recurse_to_child_object(
        obj=testpackage, child_obj=subtestpackage
    )


@pytest.mark.parametrize(
    "subpackages, modules", itertools.product([True, False], [True, False])
)
def test_recusion_subpackages_never_up(subpackages, modules):
    """As a fail-safe, we assure that recursion will never go up."""

    traverser = ObjectTraverser(subpackages=subpackages, modules=modules)
    # Notice that the arguments are switched and in the wrong order
    assert not traverser.recurse_to_child_object(
        obj=subtestpackage, child_obj=testpackage
    )


@pytest.mark.parametrize(
    "subpackages, modules", itertools.product([True, False], [True, False])
)
def test_recusion_never_other_packages(subpackages, modules):
    """While inspect.getmembers(module) yields `operator` if `import operator` is
    present in `module.py`, we should never recurse to that child."""

    traverser = ObjectTraverser(subpackages=subpackages, modules=modules)
    # Notice that the arguments are switched and in the wrong order
    assert not traverser.recurse_to_child_object(obj=module, child_obj=operator)


@pytest.mark.parametrize("subpackages", [True, False])
def test_recusion_modules(subpackages):
    """Regardless of what the `subpackages` flag says, the following should hold."""

    traverser = ObjectTraverser(subpackages=subpackages, modules=True)
    assert traverser.recurse_to_child_object(obj=testpackage, child_obj=module)

    traverser = ObjectTraverser(subpackages=subpackages, modules=False)
    assert not traverser.recurse_to_child_object(obj=testpackage, child_obj=module)


@pytest.mark.parametrize(
    "subpackages, modules", itertools.product([True, False], [True, False])
)
def test_recusion_to_objs_only_where_defined(subpackages, modules):
    """Do not recurse to objects defined elsewhere (unless we're in __init__.py).
    """
    from treedoctestpackage import module
    from treedoctestpackage.module2 import SuperClass

    traverser = ObjectTraverser(subpackages=subpackages, modules=modules)
    assert not traverser.recurse_to_child_object(obj=module, child_obj=SuperClass)


@pytest.mark.parametrize("subpackages", [True, False])
def test_recursion_objs_same_level(subpackages):
    """Test discover of object imported into __init__.py, defined at same level.
    
    Consider the structure:
        __init__.py (`MyClass` imported into here)
        module.py (`MyClass` defined here)
        
    If recursion to modules is activated, we discover module.py:MyClass.
    If recursion to modules it NOT activated, we discover it as __init__.py:MyClass.
    """
    import treedoctestpackage
    from treedoctestpackage.module import MyClass

    # =============================================================================
    #     `MyClass` is defined at the same level, not in __init__.py, but imported
    # =============================================================================

    # Recurse if it would not have been found elsewhere and it's in __init__.py
    assert MyClass in [obj for (_, obj) in inspect.getmembers(treedoctestpackage)]
    traverser = ObjectTraverser(subpackages=subpackages, modules=False)
    assert traverser.recurse_to_child_object(obj=treedoctestpackage, child_obj=MyClass)

    # It would've been found eventually, so don't discover it in __init__.py
    traverser = ObjectTraverser(subpackages=subpackages, modules=True)
    assert not traverser.recurse_to_child_object(
        obj=treedoctestpackage, child_obj=MyClass
    )


@pytest.mark.parametrize("modules", [True, False])
def test_recursion_objs_lower_level(modules):
    """Test discover of object imported into __init__.py, defined at at lower level.
    
    Consider the structure:
        __init__.py (`func_subtraction` imported into here)
        subpackage/subpackagemodule.py (`func_subtraction` defined here)
        
    If recursion to subpackages is activated, we discover 
        subpackage/subpackagemodule.py:func_subtraction.
        
    If recursion to subpackages it NOT activated, we discover 
        it as __init__.py:func_subtraction.
    """
    import treedoctestpackage
    from treedoctestpackage.subpackage.subpackagemodule import func_subtraction

    # =============================================================================
    #     `func_subtraction` is defined at a lower level, and import in __init__.py
    # =============================================================================

    # Recurse if it would not have been found elsewhere and it's in __init__.py
    assert func_subtraction in [
        obj for (_, obj) in inspect.getmembers(treedoctestpackage)
    ]
    traverser = ObjectTraverser(subpackages=False, modules=modules)
    assert traverser.recurse_to_child_object(
        obj=treedoctestpackage, child_obj=func_subtraction
    )

    # It would've been found eventually, so don't discover it in __init__.py
    traverser = ObjectTraverser(subpackages=True, modules=modules)
    assert not traverser.recurse_to_child_object(
        obj=treedoctestpackage, child_obj=func_subtraction
    )


@pytest.mark.parametrize(
    "subpackages, modules", itertools.product([True, False], [True, False])
)
def test_recursion_composite_classes(subpackages, modules):
    """We do not recurse to composite classes, i.e. from Car to it's Wheel.
    Instead we find the wheel class from it's module."""
    from treedoctestpackage.module2 import Car, Wheel
    from treedoctestpackage import module2

    traverser = ObjectTraverser(subpackages=subpackages, modules=modules)
    assert traverser.recurse_to_child_object(obj=module2, child_obj=Car)
    assert traverser.recurse_to_child_object(obj=module2, child_obj=Wheel)

    assert not traverser.recurse_to_child_object(obj=Car, child_obj=Wheel)


if __name__ == "__main__":
    import pytest

    pytest.main(args=[".", "--doctest-modules", "-v", "--capture=sys"])
