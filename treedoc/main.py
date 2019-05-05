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

    printer = printer(signature=signature, docstring=docstring)
    traverser = ObjectTraverser(
        level=level, private=private, magic=magic, stream=stream
    )

    iterable = traverser.search(obj)
    iterable = iter(iterable)

    for row in printer.format_iterable(iterable):
        if row is not None:
            print(row)


def setup_argumentparser():
    """Set up the argument parser and return it before parsing arguments."""

    parser = argparse.ArgumentParser(
        prog="treedoc",  # The name of the program
        description="Minimalistic documentation in a tree structure.",
        epilog="Report issues and contribute on https://github.com/tommyod/treedoc.",
        allow_abbrev=True,
        # add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("obj", default=None, nargs="?", help=("The object"))

    # =============================================================================
    #     OPTIONS RELATED TO OBJECT TRAVERSAL AND RECURSION
    # =============================================================================

    traversal = parser.add_argument_group(
        "traversal", "The arguments are common to every printer."
    )
    traversal.add_argument(
        "-d",
        "--depth",
        default=999,
        dest="depth",
        nargs="?",
        type=int,
        help="descend no more than DEPTH levels in the object tree.",
    )

    traversal.add_argument(
        "-sub",
        "--subpackages",
        default=False,
        dest="subpackages",
        action="store_true",
        help="descend into subpackages, i.e. numpy -> numpy.linalg",
    )

    traversal.add_argument(
        "-mod",
        "--modules",
        default=False,
        dest="submodules",
        action="store_true",
        help="descend into every module in a package.",
    )

    traversal.add_argument(
        "-p",
        "--private",
        default=False,
        dest="private",
        action="store_true",
        help="show private objects, i.e. _func(x).",
    )

    traversal.add_argument(
        "-m",
        "--magic",
        default=False,
        dest="magic",
        action="store_true",
        help="show magic methods, i.e. __add(self, other)__.",
    )

    traversal.add_argument(
        "-t",
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
        "printing", "The meaning of the arguments varies depending on the printer.\nNumeric arguments default to their middle value."
    )

    printers = {"simple": SimplePrinter, "dense": lambda x: x ** 2}
    printing.add_argument(
        "--printer",
        default="simple",
        dest="printer",
        nargs="?",
        choices=list(printers.keys()),
                help="how much signature information to show.\noptions = {}. default = {}".format(
            list(printers.keys()), "tree"
        ),
    )

    choices = (0, 1, 2)
    printing.add_argument(
        "-s",
        "--signature",
        action="store",
        default=1,
        dest="signature",
        type=int,
        choices=[0, 1, 2],
        help="how much signature information to show."
    )

    printing.add_argument(
        "-doc",
        "--docstring",
        action="store",
        default=2,
        dest="docstring",
        type=int,
        choices=[0, 1, 2, 3, 4],
        help="how much docstring information to show.",
    )

    printing.add_argument(
            "-i",
        "--info",
        action="store",
        default=2,
        dest="info",
        type=int,
        choices=[0, 1, 2, 3, 4],
        help="how much general information to show.",
    )

    return parser


def main():
    """
    Endpoint for CLI implementation.
    """
    parser = setup_argumentparser()

    printers = {"simple": SimplePrinter, "dense": lambda x: x ** 2}

    args = parser.parse_args()
    args_to_func = {k: w for (k, w) in args._get_kwargs()}
    args_to_func["printer"] = printers[args_to_func["printer"]]

    treedoc(**args_to_func)


if __name__ == "__main__":
    main()
