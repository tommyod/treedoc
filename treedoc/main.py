#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High level functions: treedoc-function, argument parsing and CLI entrypoint.
"""


import argparse
import sys

from treedoc.printing import DensePrinter, TreePrinter, resolve_input
from treedoc.traversal import ObjectTraverser
from treedoc.utils import get_terminal_size


def treedoc(
    obj,
    *,
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
    """Print minimalistic tree-like documentation.
    
    Arguments
    ---------
    obj
        A string representing an object, or several space-separated objects, or a list
        of objects. Examples: "dict", "dict set", [dict, set]
    
    Examples
    --------
    >>> treedoc(list)
    >>> treedoc("collections.Counter")
    """

    # A zero means that no width was explicitly set, if so we set it to terminal width
    if width == 0:
        width, _ = get_terminal_size(fallback=(128, 24))

    # Resolve the object
    objects = resolve_input(obj)

    # Pass the arguments to the object traverser and the printer
    traverser = ObjectTraverser(
        level=level,
        subpackages=subpackages,
        modules=modules,
        private=private,
        dunders=dunders,
        tests=tests,
        stream=stream,
    )
    printer = printer(signature=signature, docstring=docstring, info=info, width=width)

    for obj in objects:
        search_result_iterator = traverser.search(obj=obj)

        for row in printer.format_iterable(search_result_iterator):
            print(row, file=stream)


def setup_argumentparser(printers):
    """Set up the argument parser."""

    parser = argparse.ArgumentParser(
        prog="treedoc",  # The name of the program
        description="Minimalistic Python documentation for dendrophiles.",
        epilog="Report issues and contribute at https://github.com/tommyod/treedoc.",
        allow_abbrev=True,
        # add_help=True,
    )

    parser.add_argument(
        "obj",
        default="builtins",  # TODO: Change this to a different default?
        nargs="*",
        help="package/class/method/... , e.g. collections.Counter",
    )

    parser.add_argument(
        "-v",
        "--version",
        default=False,
        dest="version",
        action="store_true",
        help="print the version and exit.",
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
        "-p",
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
        help="printer to use, defaults to 'tree'",
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
        default=0,
        dest="width",
        type=int,
        # choices=range(50, 500),
        help="maximal width of the output.",
    )

    return parser


def CLI_entrypoint():
    """Set up argumentparser and parse arguments, then pass arguments to treedoc."""
    printers = {"tree": TreePrinter, "dense": DensePrinter}
    parser = setup_argumentparser(printers)

    args = parser.parse_args()

    # The user wants to print the version. Print it and exit.
    if args.version:
        from treedoc import __version__

        print("treedoc version {}".format(__version__))
        return
    else:
        delattr(args, "version")

    args_to_func = {k: w for (k, w) in args._get_kwargs()}
    args_to_func["printer"] = printers[args_to_func["printer"]]

    treedoc(**args_to_func)


if __name__ == "__main__":
    import pytest

    pytest.main(args=[".", "--doctest-modules", "-v", "--capture=sys"])
