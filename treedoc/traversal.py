#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recursive traversal of objects.
"""

import inspect
import sys
import time

from treedoc.utils import (is_inspectable, is_magic_method, is_private,
                           ispropersubpackage, recurse_on)

time = time


class ObjectTraverser:
    """Traverse Python objects, modules and packages recursively."""

    _ignored_names = set(["__class__", "__doc__", "__hash__", "builtins"])

    def __init__(
        self, *, level=999, private=False, magic=False, stream=sys.stdout, **kwargs
    ):
        self.level = level
        self.sort_key = None
        self.private = private
        self.magic = magic
        self.stream = stream

    def search(self, obj):
        """DFS search from an object."""
        yield from self._search(obj, stack=None)

    def _p(self, *args):
        """Printing/logging method."""
        # TODO: set up proper logging
        return None
        print(*args, file=self.stream)

    def _search(self, obj, stack=None, final_node_at_depth=None):
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

        self._p(f"yield_data({obj}, stack={stack})")

        if len(stack) > self.level + 1:
            return

        stack.append(obj)

        assert len(stack) == len(final_node_at_depth)
        yield stack, final_node_at_depth

        if not recurse_on(obj):
            stack.pop()
            final_node_at_depth.pop()
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
        filtered = []

        # Iterate through children
        for name, child_obj in sorted(inspect.getmembers(obj), key=self.sort_key):

            # time.sleep(0.001)
            self._p(f"Looking at {name}, {type(child_obj)}")

            try:
                getattr(child_obj, "__name__")
            except AttributeError:
                try:
                    setattr(child_obj, "__name__", name)
                except AttributeError:
                    # This is for everything to work with properties, df.DataFrame.T
                    # TODO: Figure out how to deal with properties
                    obj_name = name
                    obj_name = obj_name
                    continue

            # Only consider magic methods and private objects if the user wants to
            if is_private(child_obj) and not self.private:
                self._p(
                    f"Skipping because {obj.__name__} is private and we're not showing those."
                )
                continue

            if is_magic_method(child_obj) and not self.magic:
                self._p(
                    f"Skipping because {obj.__name__} is magic and we're not showing those."
                )
                continue

            if name in self._ignored_names:
                continue

            if not is_inspectable(child_obj):
                self._p(f" {name} was not interesting")
                pass
                # continue

            # Prevent recursing into modules
            # TODO: Generalize this
            if inspect.ismodule(obj) and inspect.ismodule(child_obj):

                if not ispropersubpackage(child_obj, obj):
                    continue

                self._p(f" Both {name} and {obj.__name__} are modules")
                self._p(
                    f" Packages: {child_obj.__package__} and {obj.__package__} are modules"
                )

                if obj.__package__ == child_obj.__package__:
                    continue

                if child_obj.__package__ in obj.__package__:
                    continue

            # We're dealing with a class imported from another library, skip it
            if inspect.isclass(child_obj) and not inspect.getmodule(
                child_obj
            ).__name__.startswith(obj.__name__):
                self._p(
                    f"{name} - {child_obj.__module__} - {inspect.getmodule(child_obj).__name__} - {obj.__name__}"
                )
                continue

            # This prevent recursing to superclasses
            if inspect.isclass(child_obj):
                self._p(
                    f" The MRO of {name} is {inspect.getmro(child_obj)}. Parent is {obj.__name__}"
                )
                self._p(f"{name} is a class: {inspect.isclass(child_obj)}")
                self._p(f"{obj.__name__} is a class: {inspect.isclass(obj)}")
            if inspect.isclass(child_obj) and obj in inspect.getmro(child_obj):
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
                stack=stack,
                final_node_at_depth=final_node_at_depth + [last],
            )

        stack.pop()
        final_node_at_depth.pop()


if __name__ == "__main__":

    import pytest

    pytest.main(args=[".", "--doctest-modules", "-v", "--capture=sys"])

    import subprocess

    subprocess.call(["treedoc", "collections"])
    subprocess.call(["treedoc", "pandas"])
    subprocess.call(["treedoc", "list"])
