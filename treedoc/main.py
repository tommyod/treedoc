#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrypoint for command line interface.
"""


import argparse
import sys

from treedoc.printing import SimplePrinter, TreePrinter
from treedoc.traversal import ObjectTraverser
from treedoc.utils import resolve_object


def treedoc(
    obj,
    level=999,
    subpackages=True,
    submodules=False,
    private=False,
    magic=False,
    tests=False,
    signature=1,
    docstring=2,
    info=2,
    printer=SimplePrinter,
    stream=sys.stdout,
):
    """
    Print minimalistic tree-like documentation.
    """

    printer = TreePrinter

    if isinstance(obj, str):
        obj = resolve_object(obj)

    if obj is None:
        raise ValueError("Could not resolve object")

    printer = printer(signature=signature, docstring=docstring, info=info)
    traverser = ObjectTraverser(
        level=level, private=private, magic=magic, stream=stream
    )

    iterable = traverser.search(obj)
    iterable = iter(iterable)

    for row in printer.format_iterable(iterable):
        if row is not None:
            print(row)


def main():
    """
    Endpoint for CLI implementation.
    """

    parser = argparse.ArgumentParser(
        prog="treedoc",  # The name of the program
        description="Minimalistic documentation in a tree structure.",
        epilog="Report issues and contribute on https://github.com/tommyod/treedoc.",
        allow_abbrev=True,
        # add_help=True,
    )

    parser.add_argument("obj", default=None, nargs="?", help=("The object"))

    # =============================================================================
    #     OPTIONS RELATED TO OBJECT TRAVERSAL AND RECURSION
    # =============================================================================

    traversal = parser.add_argument_group(
        "traversal", "The arguments are common to every printer."
    )
    traversal.add_argument(
        "--level",
        default=999,
        dest="level",
        nargs="?",
        type=int,
        help="descend only level directories deep.",
    )

    traversal.add_argument(
        "--subpackages",
        default=False,
        dest="subpackages",
        action="store_true",
        help="descend into subpackages, i.e. numpy -> numpy.linalg",
    )

    traversal.add_argument(
        "--modules",
        default=False,
        dest="submodules",
        action="store_true",
        help="descend into every module in a package.",
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
        "--tests",
        default=False,
        dest="tests",
        action="store_true",
        help="show tests, i.e. test_func().",
    )

    # =============================================================================
    #     OPTIONS RELATED TO PRINTING THE RESULTS
    # =============================================================================

    printing = parser.add_argument_group(
        "printing", "The meaning of the arguments varies depending on the printer."
    )

    printers = {"simple": SimplePrinter, "dense": lambda x: x ** 2}
    printing.add_argument(
        "--printer",
        default="simple",
        dest="printer",
        nargs="?",
        choices=list(printers.keys()),
        help="printer to use, defaults to 'simple'",
    )

    printing.add_argument(
        "--signature",
        action="store",
        default=2,
        dest="signature",
        type=int,
        choices=[0, 1, 2, 3, 4],
        help="how much signature information to show.",
    )

    printing.add_argument(
        "--docstring",
        action="store",
        default=1,
        dest="docstring",
        type=int,
        choices=[0, 1, 2],
        help="how much docstring information to show.",
    )

    printing.add_argument(
        "--info",
        action="store",
        default=2,
        dest="info",
        type=int,
        choices=[0, 1, 2, 3, 4],
        help="how much general information to show.",
    )

    args = parser.parse_args()
    args_to_func = {k: w for (k, w) in args._get_kwargs()}
    args_to_func["printer"] = printers[args_to_func["printer"]]

    treedoc(**args_to_func)


if __name__ == "__main__":
    main()
