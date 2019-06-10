#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test the command line interface (CLI).
"""
import itertools
import random
import subprocess

import pytest

object_strings = [
    "list",
    "collections",
    "collections.Counter",
    "math",
    "collections.abc.Collection",
    "list set dict",
    "list   set dict  ",
]


@pytest.mark.parametrize("obj_string", object_strings)
def test_cli_smoketests(obj_string):
    """The smoketests assure that the commands run without errors. No output testing
    is performed apart from the non-existence of an error."""

    exit_code, output = subprocess.getstatusoutput(" ".join(["treedoc", obj_string]))

    # Zero exit code means everything is OK
    assert exit_code == 0


packages = ["numpy", "scipy", "pandas", "sklearn"]


@pytest.mark.parametrize("library", packages)
def test_cli_smoketests_famous_packages(library):
    """The smoketests assure that the commands run without errors. No output testing
    is performed apart from the non-existence of an error."""

    args = " ".join(["treedoc", library, "--subpackages"])
    exit_code, output = subprocess.getstatusoutput(args)

    # Zero exit code means everything is OK
    assert exit_code == 0


def _generate_cli_args(n):
    """Generate n args."""
    random.seed(42)

    yielded = set()

    for _ in range(n):

        to_yield = " ".join(
            [
                "--level " + str(random.choice([1, 2, 3])),
                random.choice(["", "--subpackages"]),
                random.choice(["", "--modules"]),
                random.choice(["", "--private"]),
                random.choice(["", "--tests"]),
                random.choice(["--printer tree", "--printer dense"]),
                "--signature " + str(random.choice([0, 1, 2, 3, 4])),
                "--docstring " + str(random.choice([0, 1, 2])),
                "--info " + str(random.choice([0, 1, 2])),
            ]
        )
        if to_yield not in yielded:
            yielded.add(to_yield)
            yield to_yield


@pytest.mark.parametrize(
    "arg_string",
    [
        " ".join([i, j])
        for i, j in itertools.product(object_strings, _generate_cli_args(2))
    ],
)
def test_cli_smoketests_w_args(arg_string):
    """The smoketests assure that the commands run without errors. No output testing
    is performed apart from the non-existence of an error."""

    exit_code, output = subprocess.getstatusoutput(" ".join(["treedoc", arg_string]))
    assert exit_code == 0


if __name__ == "__main__":
    pytest.main(args=[__file__, "--doctest-modules", "-v", "--capture=sys"])
