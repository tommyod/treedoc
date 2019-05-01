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
        self, *, depth=999, private=False, magic=False, stream=sys.stdout, **kwargs
    ):
        self.depth = depth
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

    def _search(self, obj, stack=None):
        """
        """

        # If None, create an empty stack
        stack = stack or []

        self._p(f"yield_data({obj}, stack={stack})")

        # Abort immediately if no name is found on the object
        try:
            getattr(obj, "__name__")
        except AttributeError:
            return

        # Only consider magic methods and private objects if the user wants to
        if is_private(obj) and not self.private:
            self._p(
                f"Skipping because {obj.__name__} is private and we're not showing those."
            )
            return

        if is_magic_method(obj) and not self.magic:
            self._p(
                f"Skipping because {obj.__name__} is magic and we're not showing those."
            )
            return

        stack.append(obj)

        if len(stack) > self.depth + 1:
            stack.pop()
            return

        yield stack

        if not recurse_on(obj):
            stack.pop()
            return

        for name, attribute in sorted(inspect.getmembers(obj), key=self.sort_key):

            # time.sleep(0.001)
            self._p(f"Looking at {name}, {type(attribute)}")

            if name in self._ignored_names:
                continue

            if not is_inspectable(attribute):
                self._p(f" {name} was not interesting")
                pass
                # continue

            # Prevent recursing into modules
            # TODO: Generalize this
            if inspect.ismodule(obj) and inspect.ismodule(attribute):

                if not ispropersubpackage(attribute, obj):
                    continue

                self._p(f" Both {name} and {obj.__name__} are modules")
                self._p(
                    f" Packages: {attribute.__package__} and {obj.__package__} are modules"
                )

                if obj.__package__ == attribute.__package__:
                    continue

                if attribute.__package__ in obj.__package__:
                    continue

            # We're dealing with a class imported from another library, skip it
            if inspect.isclass(attribute) and not inspect.getmodule(
                attribute
            ).__name__.startswith(obj.__name__):
                self._p(
                    f"{name} - {attribute.__module__} - {inspect.getmodule(attribute).__name__} - {obj.__name__}"
                )
                continue

            try:
                getattr(attribute, "__name__")
            except AttributeError:
                try:
                    setattr(attribute, "__name__", name)
                except AttributeError:
                    # This is for everything to work with properties, df.DataFrame.T
                    # TODO: Figure out how to deal with properties
                    obj_name = name
                    obj_name = obj_name
                    continue

            # This prevent recursing to superclasses
            if inspect.isclass(attribute):
                self._p(
                    f" The MRO of {name} is {inspect.getmro(attribute)}. Parent is {obj.__name__}"
                )
                self._p(f"{name} is a class: {inspect.isclass(attribute)}")
                self._p(f"{obj.__name__} is a class: {inspect.isclass(obj)}")
            if inspect.isclass(attribute) and obj in inspect.getmro(attribute):
                continue

            yield from self._search(obj=attribute, stack=stack)

        stack.pop()
