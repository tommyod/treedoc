#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrypoint for command line interface.
"""


import argparse
import sys

from treedoc.printing import SimplePrinter
from treedoc.traversal import ObjectTraverser
from treedoc.utils import resolve_object


def treedoc(
    object,
    depth=999,
    subpackages=True,
    submodules=False,
    private=False,
    magic=False,
    tests=False,
    signature=1,
    docstring=1,
    printer=SimplePrinter,
    stream=sys.stdout,
):
    """
    Print minimalistic tree-like documentation.
    """

    if isinstance(object, str):
        obj = resolve_object(object)

    printer = printer(signature=signature, docstring=docstring)
    traverser = ObjectTraverser(depth=depth, private=private, magic=magic, stream=stream)

    for row in traverser.search(obj):
        row = printer.print_row(row)
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
        "--depth", default=999, dest="depth", nargs="?", type=int, help="the depth"
    )

    traversal.add_argument(
        "--subpackages",
        default=False,
        dest="subpackages",
        action="store_true",
        help="recurse into sub-packages.",
    )

    traversal.add_argument(
        "--modules",
        default=False,
        dest="submodules",
        action="store_true",
        help="recurse into sub-packages and sub-modules.",
    )

    traversal.add_argument(
        "--private",
        default=False,
        dest="private",
        action="store_true",
        help="show private objects, i.e. _func(x).",
    )

    traversal.add_argument(
        "--magic",
        default=False,
        dest="magic",
        action="store_true",
        help="show magic methods, i.e. __add(self, other)__.",
    )

    traversal.add_argument(
        "--tests", default=False, dest="tests", action="store_true", help="show tests."
    )

    # =============================================================================
    #     OPTIONS RELATED TO PRINTING THE RESULTS
    # =============================================================================

    printing = parser.add_argument_group("printing")

    printers = {"simple": SimplePrinter, "dense": lambda x: x ** 2}
    printing.add_argument(
        "--printer",
        default="simple",
        dest="printer",
        nargs="?",
        choices=list(printers.keys()),
        help="Printer to use.",
    )

    parser.add_argument(
        "--signature",
        action="store",
        default=1,
        dest="signature",
        type=int,
        choices=[0, 1, 2],
        help="How much signature information to show.",
    )

    parser.add_argument(
        "--docstring",
        action="store",
        default=1,
        dest="docstring",
        type=int,
        choices=[0, 1, 2, 3, 4, 5],
        help="How much docstring information to show.",
    )

    args = parser.parse_args()
    args_to_func = {k: w for (k, w) in args._get_kwargs()}
    args_to_func['printer'] = printers[args_to_func['printer']]

    treedoc(**args_to_func)


if __name__ == "__main__":
    main()
