#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrypoint for command line interface.
"""


import argparse
import sys

from treedoc.printing import DensePrinter, TreePrinter
from treedoc.traversal import ObjectTraverser
from treedoc.utils import resolve_input


def treedoc(
    *,
    obj,
    level=999,
    subpackages=False,
    modules=False,
    private=False,
    dunders=False,
    tests=False,
    signature=1,
    docstring=2,
    info=2,
    width=88,
    printer=TreePrinter,
    stream=sys.stdout,
):
    """
    Print minimalistic tree-like documentation.
    """

    objects = resolve_input(obj)

    printer = printer(signature=signature, docstring=docstring, info=info, width=width)
    traverser = ObjectTraverser(
        level=level,
        subpackages=subpackages,
        modules=modules,
        private=private,
        dunders=dunders,
        stream=stream,
    )

    for obj in objects:
        iterable = traverser.search(obj=obj)
        iterable = iter(iterable)

        for row in printer.format_iterable(iterable):
            if row is not None:
                print(row, file=stream)


def setup_argumentparser(printers):
    """
    Endpoint for CLI implementation.
    """

    parser = argparse.ArgumentParser(
        prog="treedoc",  # The name of the program
        description="Minimalistic Python documentation in a tree structure.",
        epilog="Report issues and contribute at https://github.com/tommyod/treedoc.",
        allow_abbrev=True,
        # add_help=True,
    )

    parser.add_argument(
        "obj",
        default=None,
        nargs="?",
        help="package/class/method/... , e.g. collections.Counter",
    )

    # =============================================================================
    #     OPTIONS RELATED TO OBJECT TRAVERSAL AND RECURSION
    # =============================================================================

    traversal = parser.add_argument_group(
        "traversal", "The arguments below are common to every printer."
    )
    traversal.add_argument(
        "-l",
        "--level",
        default=999,
        dest="level",
        nargs="?",
        type=int,
        help="descend only level directories deep.",
    )

    traversal.add_argument(
        "-s",
        "--subpackages",
        default=False,
        dest="subpackages",
        action="store_true",
        help="descend into subpackages, i.e. numpy -> numpy.linalg",
    )

    traversal.add_argument(
        "-m",
        "--modules",
        default=False,
        dest="modules",
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
        "-d",
        "--dunders",
        default=False,
        dest="dunders",
        action="store_true",
        help="show double underscore methods, i.e. __add__(self, other).",
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
        "printing",
        "The meaning of the arguments below may vary depending on the printer.\nNumeric arguments default to middle values, printer defaults to 'tree'.",
    )

    printing.add_argument(
        "-P",
        "--printer",
        default="tree",
        dest="printer",
        nargs="?",
        choices=list(printers.keys()),
        help="printer to use, defaults to 'simple'",
    )

    printing.add_argument(
        "-S",
        "--signature",
        action="store",
        default=2,
        dest="signature",
        type=int,
        choices=[0, 1, 2, 3, 4],
        help="how much signature information to show.",
    )

    printing.add_argument(
        "-D",
        "--docstring",
        action="store",
        default=1,
        dest="docstring",
        type=int,
        choices=[0, 1, 2],
        help="how much docstring information to show.",
    )

    printing.add_argument(
        "-I",
        "--info",
        action="store",
        default=2,
        dest="info",
        type=int,
        choices=[0, 1, 2, 3, 4],
        help="how much general information to show.",
    )

    printing.add_argument(
        "-W",
        "--width",
        action="store",
        default=88,
        dest="width",
        type=int,
        choices=range(50, 500),
        help="maximal width of the output.",
    )

    return parser


def main():
    """TODO
    """
    printers = {"tree": TreePrinter, "dense": DensePrinter}
    parser = setup_argumentparser(printers)

    args = parser.parse_args()
    args_to_func = {k: w for (k, w) in args._get_kwargs()}
    args_to_func["printer"] = printers[args_to_func["printer"]]

    treedoc(**args_to_func)


if __name__ == "__main__":
    main()
