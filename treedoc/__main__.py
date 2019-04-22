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

    parser = argparse.ArgumentParser(description="Process some integers.")

    parser.add_argument(
        "object", metavar="PROJECT_DIR", default=None, nargs="?", help=("output path")
    )

    args = parser.parse_args()

    try:
        obj = importlib.import_module(args.object)
    except ModuleNotFoundError:
        obj = eval(args.object)

    traverser = ObjectTraverser()

    for row in traverser.search(obj):
        row = simpleprint(row)
        if row is not None:
            print(row)


if __name__ == "__main__":
    main()
