#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrypoint for command line interface.
"""


import argparse
import importlib
from treedoc.traversal import ObjectTraverser
from treedoc.printing import simpleprint


def treedoc(obj):
    pass


def main(*args, **kwargs):

    parser = argparse.ArgumentParser(
        description="Minimalistic documentation in a tree structure."
    )

    parser.add_argument("object", default=None, nargs="?", help=("The object"))

    # =============================================================================
    #     OPTIONS RELATED TO OBJECT TRAVERSAL AND RECURSION
    # =============================================================================

    traversal = parser.add_argument_group("traversal")
    traversal.add_argument(
        "-D", "--depth", default=999, dest="depth", nargs="?", help=("The depth")
    )
    traversal.add_argument(
        "-P",
        "--packages",
        default=False,
        dest="sub_packages",
        action="store_true",
        help=("Recurse into sub-packages."),
    )
    traversal.add_argument(
        "-M",
        "--modules",
        default=False,
        dest="sub_modules",
        action="store_true",
        help=("Recurse into sub-modules."),
    )

    # =============================================================================
    #     OPTIONS RELATED TO PRINTING THE RESULTS
    # =============================================================================

    printing = parser.add_argument_group("printing")
    printing.add_argument(
        "-p",
        "--private",
        default=False,
        dest="private",
        action="store_true",
        help=("Show private objects, i.e. _func(x)."),
    )
    printing.add_argument(
        "-m",
        "--magic",
        default=False,
        dest="magic",
        action="store_true",
        help=("Show magic methods, i.e. __add(self, other)__."),
    )

    printers = {"simple": lambda x: x ** 2, "dense": lambda x: x ** 2}
    printing.add_argument(
        "--printer",
        default=None,
        dest="printer",
        nargs="?",
        help=("Printer to use: {}.".format(", ".join(printers.keys()))),
    )

    args = parser.parse_args()

    try:
        obj = importlib.import_module(args.object)
    except ModuleNotFoundError:
        try:
            obj = eval(args.object)
        except:
            *start, final = args.object.split(".")
            start = ".".join(start)

            mod = __import__(start, fromlist=[final])
            obj = getattr(mod, final)

            # eval("from {} import {} as obj".format(start, final))

    traverser = ObjectTraverser()

    for row in traverser.search(obj):
        row = simpleprint(row)
        if row is not None:
            print(row)


if __name__ == "__main__":
    main()
