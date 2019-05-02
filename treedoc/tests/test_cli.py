#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test the command line interface.
"""
import subprocess

import pytest


@pytest.mark.parametrize(
    "obj_string",
    [
        "list",
        "collections",
        "collections.Counter",
        "math",
        "collections.abc.Collection",
    ],
)
def test_cli_smoketests(obj_string):
    """The smoketests assure that the commands run without errors. No output testing
    is performed apart from the non-existence of an error."""

    exit_code, output = subprocess.getstatusoutput(" ".join(["treedoc", obj_string]))

    # Zero exit code means everything is OK
    assert exit_code == 0


if __name__ == "__main__":
    pytest.main(args=[__file__, "--doctest-modules", "-v", "--capture=sys"])
