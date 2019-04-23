#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrypoint for command line interface.
"""


import argparse
import sys

from treedoc.printing import simpleprint
from treedoc.traversal import ObjectTraverser
from treedoc.utils import resolve_object


def treedoc(
    object,
    depth=999,
    sub_packages=True,
    sub_modules=False,
    private=False,
    magic=False,
    printer=simpleprint,
    stream=sys.stdout,
):
    """
    Print minimalistic tree-like documentation.
    """

    if isinstance(object, str):
        obj = resolve_object(object)

    traverser = ObjectTraverser()

    for row in traverser.search(obj):
        row = simpleprint(row)
        if row is not None:
            print(row, file=sys.stdout)


def main():
    """
    Endpoint for CLI implementation.
    """

    parser = argparse.ArgumentParser(
        prog="treedoc",  # The name of the program
        description="Minimalistic documentation in a tree structure.",
        epilog="Contribute on ",  # Text following the argument descriptions
        allow_abbrev=True,
        add_help=True,
    )

    parser.add_argument("object", default=None, nargs="?", help=("The object"))

    # =============================================================================
    #     OPTIONS RELATED TO OBJECT TRAVERSAL AND RECURSION
    # =============================================================================

    traversal = parser.add_argument_group("traversal")
    traversal.add_argument(
        "-D",
        "--depth",
        default=999,
        dest="depth",
        nargs="?",
        type=int,
        help=("The depth"),
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
        help=("Recurse into sub-packages and sub-modules."),
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
    args_to_func = {k: w for (k, w) in args._get_kwargs()}

    treedoc(**args_to_func)


if __name__ == "__main__":
    main()
