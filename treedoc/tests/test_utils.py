#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for classes and functions located in `utils.py`.
"""


if __name__ == "__main__":
    import pytest

    # --durations=10  <- May be used to show potentially slow tests
    pytest.main(args=[__file__, "--doctest-modules", "-v", "--capture=sys"])
