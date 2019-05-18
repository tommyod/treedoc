#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for traversal of objects.



                   +---+                  
      -------------|obj|--------------    
      |            +---+             |    
      |              |               |    
      v              v               v    
+----------+   +----------+   +----------+
|child_obj1|   |child_obj2|   |child_obj3|
+----------+   +----------+   +----------+


"""
import inspect
import itertools
import os
import functools
import importlib
import pkgutil
import sys
from treedoc.utils_meta import PrintMixin


# =============================================================================
# ------------------------ PART 1/2 OF MODULE - CLASSES -----------------------
# =============================================================================


class ObjectTraverser(PrintMixin):
    """Traverse Python objects, modules and packages recursively."""

    _ignored_names = set(["__class__", "__doc__", "__hash__", "builtins", "__cached__"])

    def __init__(
        self,
        *,
        level=999,
        subpackages=False,
        modules=False,
        private=False,
        dunders=False,
        tests=False,
        stream=sys.stdout,
    ):
        self.level = level
        self.subpackages = subpackages
        self.modules = modules
        self.sort_key = None
        self.private = private
        self.dunders = dunders
        self.tests = tests
        self.stream = stream

    def search(self, obj):
        """DFS search starting at an object and recursing to its children."""
        yield from self._search(obj=obj, stack=None)

    def _p(self, *args):
        """Printing/logging method."""
        return None
        # TODO: set up proper logging
        print(*args, file=self.stream)

    def recurse_to_child_object(self, *, obj, child_obj):
        """Given an object and it's child, do we recurse down to the child?"""

        self._p(f"obj = {obj.__name__}, child_obj = {child_obj.__name__}")

        # =============================================================================
        #  (1) CASE: Parent is a module, and child is not a module
        # =============================================================================

        if inspect.ismodule(obj) and not inspect.ismodule(child_obj):

            # Prevent `collections.eq` / `collections._eq`
            if inspect.isbuiltin(child_obj):
                if inspect.getmodule(child_obj) != obj:
                    self._p(f"Failed on condition 1.1")
                    return False

            # Not defined in the sub-tree, skip it
            if not is_subpackage(inspect.getmodule(child_obj), obj):
                self._p(f"Failed on condition 1.2")
                return False

            # The object is defined in a different file
            if inspect.getmodule(child_obj) != obj:

                # If the object is not __init__.py,
                # never include anything imported to it
                if not is_package(obj):
                    self._p(f"Failed on condition 1.3")
                    return False

                # At this point the object is __init__.py, and we *might* include
                # a file imported into it (depending on settings below)

                # The object is defined at a lower level
                if is_propersubpackage(inspect.getmodule(child_obj), obj):

                    if self.subpackages:
                        # will find it later, so skip it now
                        self._p(f"Failed on condition 1.4")
                        return False

                # If the object is defined at the same level
                if is_subpackage(inspect.getmodule(child_obj), obj) and is_subpackage(
                    obj, inspect.getmodule(child_obj)
                ):

                    if self.modules:
                        # will find it later, so skip it now
                        self._p(f"Failed on condition 1.5")
                        return False

        # =============================================================================
        #  (2) CASE: Both parent and child are modules, i.e. __init__.py or module.py
        # =============================================================================

        if inspect.ismodule(obj) and inspect.ismodule(child_obj):

            # The order is wrong, i.e. `main` in `main.subpackage` implies going up
            different_packages = child_obj.__package__ != obj.__package__
            # pytest.collect has __package__ == None
            if child_obj.__package__ is None:
                child_package_wrong = False
            else:
                child_package_wrong = child_obj.__package__ in obj.__package__
            if different_packages and child_package_wrong:
                self._p(f"Failed on condition 2.1")
                return False

            if child_obj.__package__ is not None:
                # Prevents for instance `pandas` to recurse into `numpy`
                if not obj.__package__ in child_obj.__package__:
                    self._p(f"Failed on condition 2.2")
                    return False

            # Another fail safe to prevent `mysubpackage` to recurse into `subpack`
            if hasattr(obj, "__path__") and hasattr(child_obj, "__path__"):
                # TODO
                pass

            # Fail safe to prevent recursing from `pkg/file.py` to `pkg/__init__.py`
            if hasattr(obj, "__file__") and hasattr(child_obj, "__file__"):

                obj_pth, obj_py_file = os.path.split(inspect.getfile(obj))
                child_obj_pth, child_obj_py_file = os.path.split(
                    inspect.getfile(child_obj)
                )
                if not obj_pth in child_obj_pth:
                    self._p(f"Failed on condition 2.3")
                    return False

                if inspect.getfile(obj) == inspect.getfile(child_obj):
                    self._p(f"Failed on condition 2.4")
                    return False

                if child_obj_py_file == "__init__.py" and obj_py_file != "__init__.py":
                    self._p(f"Failed on condition 2.5")
                    return False

            if is_propersubpackage(child_obj, obj) and not self.subpackages:
                self._p(f"Failed on condition 2.6")
                return False

            try:
                file = inspect.getfile(child_obj)
                if (not file.endswith("__init__.py")) and not self.modules:
                    self._p(f"Failed on condition 2.7")
                    return False
            except TypeError:
                # TypeError: <module 'sys' (built-in)> is a built-in module
                pass

            if obj.__package__ == child_obj.__package__ and not self.modules:
                self._p(f"Failed on condition 2.8")
                return False

        # =============================================================================
        #  (3) CASE: The child is a class
        # =============================================================================

        # We're dealing with a class imported from another library, skip it
        # TODO: Extend this to other objects?
        if inspect.isclass(child_obj):

            if not is_subpackage(inspect.getmodule(child_obj), obj):
                self._p(f"Failed on condition 3.1")
                return False

            if obj in inspect.getmro(child_obj):
                self._p(f"Failed on condition 3.2")
                return False

            # We prefer going from modules to classes, not from classes to classes
            if inspect.isclass(obj):
                self._p(f"Failed on condition 3.3")
                return False

        # =============================================================================
        #         if not is_subpackage(inspect.getmodule(child_obj), obj):
        #             self._p(f"Failed on condition 4.1")
        #             return False
        # =============================================================================

        return True

    def recurse_to_object(self, obj):
        """Given an object, should we recurse down to it?"""

        name = obj.__name__

        if name in self._ignored_names:
            return False

        if obj is type:
            return False

        if is_test(obj) and not self.tests:
            return False

        if is_private(obj) and not self.private:
            return False

        if is_dunder_method(obj) and not self.dunders:
            return False

        if not is_inspectable(obj):
            self._p(f"Failed on condition 4.1")
            return False

        return True

    def _search(self, *, obj, stack=None, final_node_at_depth=None):
        """
        """

        # =============================================================================
        #         (1) BOUNDARY CONDITIONS
        #         These conditions are triggered when the DFS reaches a leaf node in
        #         the object tree, when the search has reached its desired depth or
        #         at the root note of the object tree.
        # =============================================================================

        stack = stack or []
        final_node_at_depth = final_node_at_depth or [True]

        self._p(
            f"yield_data({obj}, stack={stack}), final_node_at_depth={final_node_at_depth}"
        )

        if len(stack) > self.level + 1:
            self._p(f"Max level reached. Aborting.")
            return

        assert len(stack + [obj]) == len(final_node_at_depth)
        yield stack + [obj], final_node_at_depth

        # If it's not a module/package or class, we don't bother getting children
        if not (inspect.ismodule(obj) or inspect.isclass(obj)):
            return

        # =============================================================================
        #         (2) FILTER THE CHILD OBJECTS
        #         For efficient tree-like printing it's crucial to know whether
        #         a child node is the last child to be visited _before_ the
        #         DFS search recurses. If a, b and c are children of A, then
        #         the algorithm must discover that c is the final child of A
        #         before it recurses on a, b or c. This is to facilitate
        #         efficient printing.
        # =============================================================================

        # The objects we will recurse on
        generator1 = descend_from_package(
            package=obj, include_tests=self.tests, include_private=self.private
        )
        generator2 = inspect.getmembers(obj)

        def unique_first(gen1, gen2):
            """Chain generators, but only one unique name."""
            seen = set()
            for a, b in itertools.chain(generator1, generator2):
                if a not in seen:
                    seen.add(a)
                    yield a, b

        generator = unique_first(generator1, generator2)

        # Iterate through children
        filtered = []
        for name, child_obj in sorted(generator, key=self.sort_key):

            self._p(f"Looking at {name}, {type(child_obj)}")

            try:
                getattr(child_obj, "__name__")
            except AttributeError:
                try:
                    setattr(child_obj, "__name__", name)
                except AttributeError:
                    # This is for everything to work with properties, df.DataFrame.T
                    # TODO: Figure out how to deal with properties
                    continue

            assert hasattr(child_obj, "__name__")

            # Check if we should skip the object by virtue of it's properties
            if not self.recurse_to_object(obj=child_obj):
                continue

            # Check if we should skip the child object by virtue of it's relationship
            # to the parent object
            if not self.recurse_to_child_object(obj=obj, child_obj=child_obj):
                continue

            filtered.append((name, child_obj))

        # =============================================================================
        #         (3) RECURSE ON CHILD OBJECTS
        #         For every child object that we're interested in, we recurse.
        # =============================================================================

        for num, (name, child_obj) in enumerate(filtered, 1):

            last = True if len(filtered) == num else False
            yield from self._search(
                obj=child_obj,
                stack=stack.copy() + [obj],
                final_node_at_depth=final_node_at_depth.copy() + [last],
            )
            
# =============================================================================
# ------------------------ PART 2/2 OF MODULE - FUNCTIONS ---------------------
# =============================================================================
            
            
def is_inspectable(obj):
    """An object is inspectable if it returns True for any of the inspect.is.. functions."""
    funcs = (func_name for func_name in dir(inspect) if func_name.startswith("is"))
    funcs = (getattr(inspect, func_name) for func_name in funcs)
    return any([func(obj) for func in funcs]) or isinstance(obj, functools.partial)


def is_propersubpackage(package_a, package_b):
    """
    Is A a proper subpackage or submodule of B?
    """
    try:
        path_a, _ = os.path.split(inspect.getfile(package_a))
        path_b, _ = os.path.split(inspect.getfile(package_b))
        # is a built-in module
    except TypeError:
        return False

    return (path_b in path_a) and not (path_b == path_a)


def is_subpackage(package_a, package_b):
    """
    Is A a subpackage or submodule of B?
    """
    try:
        path_a, _ = os.path.split(inspect.getfile(package_a))
        path_b, _ = os.path.split(inspect.getfile(package_b))

    except TypeError:
        # is a built-in module

        # For instance: is_subpackage(builtins, builtins) should return True
        if package_a == package_b:
            return True

        return False

    return path_b in path_a


def is_dunder_method(obj):
    # if not inspect.ismethod(obj) or inspect.ismethoddescriptor(obj) or isinstance(obj, collections.abc.Callable):
    #    return False

    assert hasattr(obj, "__name__")
    obj_name = obj.__name__
    return obj_name.endswith("__") and obj_name.startswith("__")


def is_private(obj):
    assert hasattr(obj, "__name__")
    obj_name = obj.__name__
    typical_private = obj_name.startswith("_") and obj_name[1] != "_"
    private_subpackage = "._" in obj_name
    return typical_private or private_subpackage


def is_test(obj):
    assert hasattr(obj, "__name__")
    obj_name = obj.__name__.lower()
    patterns = ("test", "_test", "__test")
    return any(obj_name.startswith(pattern) for pattern in patterns)


def is_package(obj):

    if not hasattr(obj, "__file__"):
        return False

    return obj.__file__.endswith("__init__.py")

def descend_from_package(
    package, *, types="package", include_tests=False, include_private=False
):
    """
    Descent from a package to either a subpackage or modules one level down.
    
    Yields a tuple of (object, object_name) one level down.
    """
    if not inspect.ismodule(package):
        return None

    try:
        path, _ = os.path.split(inspect.getfile(package))
        # TypeError: <module 'itertools' (built-in)> is a built-in module
    except TypeError:
        return None

    prefix = package.__name__ + "."

    generator = pkgutil.iter_modules(path=[path], prefix=prefix)

    for (importer, object_name, ispkg) in generator:

        ismodule = not ispkg

        # Covers names such as "test", "tests", "testing", ...
        if ".test" in object_name.lower() and not include_tests:
            continue

        if "._" in object_name.lower() and not include_private:
            continue

        try:
            obj = importlib.import_module(object_name)
        except ModuleNotFoundError:
            # TODO: Replace this with logging
            # print(f"Could not import {object_name}. Error: {error}")
            return
        except ImportError:
            # print(f"Could not import {object_name}. Error: {error}")
            return

        # File "/home/tommy/anaconda3/envs/treedoc/lib/python3.7/ctypes/wintypes.py", line 20, in <module>
        except ValueError:
            # print(f"Could not import {object_name}. Error: {error}")
            return

        # File "/home/tommy/anaconda3/envs/treedoc/lib/python3.7/ctypes/wintypes.py", line 20, in <module>
        except LookupError:
            # print(f"Could not import {object_name}. Error: {error}")
            return

        if types.lower() == "package" and ispkg:
            yield object_name, obj
        elif types.lower() == "module" and ismodule:
            yield object_name, obj
        elif types.lower() == "both":
            yield object_name, obj
        elif types.lower() not in ("package", "module", "both"):
            raise ValueError("Parameter `types` must be 'package', 'module' or 'both'.")






if __name__ == "__main__":
    import pytest

    pytest.main(args=[".", "--doctest-modules", "-v", "--capture=sys"])
