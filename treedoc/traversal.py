#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recursive traversal of objects.
"""

import functools
import inspect
import sys
import time
from treedoc.utils import is_magic_method, is_private

time = time


def pprint(*args, **kwargs):
    return None
    print(*args, **kwargs)


def recurse_on(obj):
    return inspect.ismodule(obj) or inspect.isclass(obj)


def is_method(obj):
    return inspect.ismethoddescriptor(obj) or inspect.ismethod(obj)


def is_bound_method(obj):
    condition1 = "." in obj.__qualname__
    if not inspect.getfullargspec(obj).args:
        return False
    condition2 = inspect.getfullargspec(obj).args[0] == "self"
    return condition1 and condition2


def is_interesting(obj):
    funcs = [getattr(inspect, method) for method in dir(inspect) if "is" == method[:2]]
    return any([func(obj) for func in funcs]) or isinstance(obj, functools.partial)


class ObjectTraverser:
    
    _ignored_names = set(["__class__", "__doc__", "__hash__", "builtins"])
    
    
    def __init__(self, *, depth=999, private=False, magic=False, stream=sys.stdout, **kwargs):
        self.depth = depth
        self.sort_key = None
        self.private = private
        self.magic = magic
        self.stream = stream
        

    def search(self, obj):
        yield from self._search(obj, stack=None)
        
    def _p(self, *args):
        return None
        print(*args, file=self.stream)

    def _search(self, obj, stack=None):
        """
        """
        
        # If None, create an empty stack
        stack = stack or []

        pprint(f"yield_data({obj}, stack={stack})")
        
        # Abort immediately if no name is found on the object
        try:
            getattr(obj, "__name__")
        except AttributeError:
            return
        
        # Only consider magic methods and private objects if the user wants to
        if (is_private(obj) and not self.private):
            self._p(f"Skipping because {obj.__name__} is private and we're not showing those.")
            return
        
        if (is_magic_method(obj) and not self.magic):
            self._p(f"Skipping because {obj.__name__} is magic and we're not showing those.")
            return
        
        stack.append(obj)
        
        if (len(stack) > self.depth + 1):
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

            if not is_interesting(attribute):
                pprint(f" {name} was not interesting")
                pass
                #continue
            
            

            # Prevent recursing into modules
            # TODO: Generalize this

            if inspect.ismodule(obj) and inspect.ismodule(attribute):
                pprint(f" Both {name} and {obj.__name__} are modules")
                continue
                # If it's not the same package, skip it
                if attribute.__package__ != obj.__package__:
                    pprint(
                        f" Both {attribute.__package__} and {obj.__package__} are modules"
                    )
                    continue

            #if inspect.isclass(obj) and inspect.isclass(attribute):
            #    continue
            #if inspect.isabstract(obj) and inspect.isabstract(attribute):
            #    continue

            # We're deatling with a class imported from another library, skip it
            if inspect.isclass(attribute) and not inspect.getmodule(attribute).__name__.startswith(obj.__name__):
                pprint(f"{name} - {attribute.__module__} - {inspect.getmodule(attribute).__name__} - {obj.__name__}")
                continue

# =============================================================================
#             if (
#                 inspect.isfunction(attribute)
#                 and not is_bound_method(attribute)
#                 and inspect.getmodule(attribute) != obj
#             ):
#                 pass
# =============================================================================

            
            try:
                getattr(attribute, "__name__")
            except AttributeError:
                try:
                    setattr(attribute, "__name__", name)
                except AttributeError:
                    # This is for everything to work with properties, df.DataFrame.T
                    obj_name = name
                    continue

            # This prevent recursing to superclasses
            if inspect.isclass(attribute):
                pprint(
                    f" The MRO of {name} is {inspect.getmro(attribute)}. Parent is {obj.__name__}"
                )
                pprint(f"{name} is a class: {inspect.isclass(attribute)}")
                pprint(f"{obj.__name__} is a class: {inspect.isclass(obj)}")
            if inspect.isclass(attribute) and obj in inspect.getmro(attribute):
                continue


            yield from self._search(obj=attribute, stack=stack)
    
# =============================================================================
#             if not recurse_on(attribute):
#                 pprint(f" Not recursing on {name}")
#                 yield stack + [attribute]
#             else:
#                 yield from self._search(obj=attribute, stack=stack)
# =============================================================================

        stack.pop()


if __name__ == "__main__":

    import KDEpy

    from printing import simpleprint

    objtrav = ObjectTraverser()
    for row in objtrav.search(KDEpy):

        print(simpleprint(row))

        # print(row[-1].__doc__)

        # print(*[c for c in row], sep="->")
        # print(*[c.__name__ for c in row], sep="->")
        # print(*[type(c) for c in row], sep="->")
        # print()
