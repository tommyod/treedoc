#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entrypoint for command line interface.
"""

import argparse
import importlib
import pkgutil
import sys

from treedoc.printing import DensePrinter, TreePrinter
from treedoc.traversal import ObjectTraverser
from treedoc.utils import resolve_object


def treedoc(
    *,
    object,
    depth=999,
    subpackages=True,
    modules=False,
    private=False,
    magic=False,
    tests=False,
    signature=1,
    docstring=2,
    info=2,
    printer=TreePrinter,
    stream=sys.stdout,
):
    """
    Print minimalistic tree-like documentation.
    """

    printer = printer(signature=signature, docstring=docstring)
    traverser = ObjectTraverser(
        depth=depth,
        subpackages=subpackages,
        modules=modules,
        private=private,
        magic=magic,
        tests=tests,
        stream=stream,
    )

    objects = []

    if isinstance(object, str) and object.lower().strip() == "python":

        for (importer, object_name, ispkg) in pkgutil.iter_modules():

            if not ispkg:
                continue

            try:
                object = importlib.import_module(object_name)
            except:
                continue

            objects.append(object)

            iterable = iter(traverser.search(object))
            for row in printer.format_iterable(iterable):
                if row is not None:
                    print(row)

    else:

        if isinstance(object, str):
            object = resolve_object(object)

        if object is None:
            raise ValueError("Could not resolve object")
        objects.append(object)

    # From here on out, we assume that objects is a list
    assert isinstance(objects, list)
    assert len(objects) > 0

    for object in objects:
        iterable = iter(traverser.search(object))

        for row in printer.format_iterable(iterable):
            if row is not None:
                print(row)


def setup_argumentparser(printers):
    """Set up the argument parser and return it before parsing arguments."""

    parser = argparse.ArgumentParser(
        prog="treedoc",  # The name of the program
        description="Minimalistic Python documentation in a tree structure.",
        epilog="Report issues and contribute on https://github.com/tommyod/treedoc.",
        allow_abbrev=True,
        # add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "object",
        default=None,
        nargs="?",
        help=("package/class/method/... , e.g. collections.Counter"),
    )

    # =============================================================================
    #     OPTIONS RELATED TO OBJECT TRAVERSAL AND RECURSION
    # =============================================================================

    traversal = parser.add_argument_group(
        "traversal", "The arguments below are common to every printer."
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
        "-s",
        "--subpackages",
        default=False,
        dest="subpackages",
        action="store_true",
        help="descend into subpackages, e.g. numpy -> numpy.linalg",
    )

    traversal.add_argument(
        "-mod",
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
        help="show private objects, e.g. _func(x).",
    )

    traversal.add_argument(
        "-m",
        "--magic",
        default=False,
        dest="magic",
        action="store_true",
        help="show magic methods, e.g. __add(self, other)__.",
    )

    traversal.add_argument(
        "-t",
        "--tests",
        default=False,
        dest="tests",
        action="store_true",
        help="show tests, e.g. test_func().",
    )

    # =============================================================================
    #     OPTIONS RELATED TO PRINTING THE RESULTS
    # =============================================================================

    printing = parser.add_argument_group(
        "printing",
        "The meaning of the arguments below may vary depending on the printer.\nNumeric arguments default to middle values, printer defaults to 'tree'.",
    )

    printing.add_argument(
        "--printer",
        default="tree",
        dest="printer",
        nargs="?",
        choices=list(printers.keys()),
        help="general output formatting style.",
    )

    printing.add_argument(
        "-sig",
        "--signature",
        action="store",
        default=1,
        dest="signature",
        type=int,
        choices=[0, 1, 2],
        help="how much signature information to show.",
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
    printers = {"tree": TreePrinter, "dense": DensePrinter}
    parser = setup_argumentparser(printers)

    args = parser.parse_args()
    args_to_func = {k: w for (k, w) in args._get_kwargs()}
    args_to_func["printer"] = printers[args_to_func["printer"]]

    treedoc(**args_to_func)


if __name__ == "__main__":
    main()
