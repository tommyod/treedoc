#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test the printers and their functionality.
"""

from treedoc.printing import TreePrinter
from treedoc.utils import Peekable


class TestTreePrinter:
    def test_row_formatting_ex1(self):
        """Test on an example drawn by hand."""

        printer = TreePrinter()

        # These can be substituted for further generalization.
        # TODO
        # =============================================================================
        #         RIGHT = "├──"
        #         DOWN = "│  "
        #         LAST = "└──"
        #         BLANK = "   "
        # =============================================================================

        rows = [
            (["root"], [True]),
            (["root", "A"], [True, False]),
            (["root", "A", "a"], [True, False, False]),
            (["root", "A", "b"], [True, False, False]),
            (["root", "A", "c"], [True, False, True]),
            (["root", "B"], [True, True]),
            (["root", "B", "a"], [True, True, False]),
            (["root", "B", "b"], [True, True, True]),
        ]

        rows = Peekable(iter(rows))
        formatted_rows = list(printer._format_row(rows))

        assert formatted_rows == [
            ([""], ["root"]),
            (["", "├──"], ["root", "A"]),
            (["", "│  ", "├──"], ["root", "A", "a"]),
            (["", "│  ", "├──"], ["root", "A", "b"]),
            (["", "│  ", "└──"], ["root", "A", "c"]),
            (["", "└──"], ["root", "B"]),
            (["", "   ", "├──"], ["root", "B", "a"]),
            (["", "   ", "└──"], ["root", "B", "b"]),
        ]

    def test_row_formatting_ex2(self):
        """Test on an example drawn by hand."""

        printer = TreePrinter()

        rows = [
            (["root"], [True]),
            (["root", "A"], [True, False]),
            (["root", "A", "a"], [True, False, False]),
            (["root", "A", "b"], [True, False, True]),
            (["root", "A", "b", "A"], [True, False, True, False]),
            (["root", "A", "b", "B"], [True, False, True, False]),
            (["root", "A", "b", "C"], [True, False, True, True]),
            (["root", "B"], [True, True]),
            (["root", "B", "a"], [True, True, False]),
            (["root", "B", "b"], [True, True, True]),
        ]

        rows = Peekable(iter(rows))
        formatted_rows = list(printer._format_row(rows))

        assert formatted_rows == [
            ([""], ["root"]),
            (["", "├──"], ["root", "A"]),
            (["", "│  ", "├──"], ["root", "A", "a"]),
            (["", "│  ", "└──"], ["root", "A", "b"]),
            (["", "│  ", "   ", "├──"], ["root", "A", "b", "A"]),
            (["", "│  ", "   ", "├──"], ["root", "A", "b", "B"]),
            (["", "│  ", "   ", "└──"], ["root", "A", "b", "C"]),
            (["", "└──"], ["root", "B"]),
            (["", "   ", "├──"], ["root", "B", "a"]),
            (["", "   ", "└──"], ["root", "B", "b"]),
        ]

    def test_row_formatting_ex3(self):
        """Test on an example drawn by hand."""

        printer = TreePrinter()

        rows = [
            (["root"], [True]),
            (["root", "A"], [True, False]),
            (["root", "B"], [True, False]),
            (["root", "C"], [True, False]),
            (["root", "C", "a"], [True, False, False]),
            (["root", "C", "b"], [True, False, False]),
            (["root", "C", "c"], [True, False, False]),
            (["root", "C", "c", "A"], [True, False, False, False]),
            (["root", "C", "c", "B"], [True, False, False, False]),
            (["root", "C", "c", "C"], [True, False, False, False]),
            (["root", "C", "c", "D"], [True, False, False, False]),
            (["root", "C", "c", "D", "a"], [True, False, False, False, False]),
            (["root", "C", "c", "D", "b"], [True, False, False, False, False]),
            (["root", "C", "c", "D", "c"], [True, False, False, False, False]),
            (["root", "C", "c", "D", "d"], [True, False, False, False, False]),
            (
                ["root", "C", "c", "D", "d", "A"],
                [True, False, False, False, False, False],
            ),
            (
                ["root", "C", "c", "D", "d", "B"],
                [True, False, False, False, False, False],
            ),
            (
                ["root", "C", "c", "D", "d", "C"],
                [True, False, False, False, False, True],
            ),
            (
                ["root", "C", "c", "D", "d", "C", "a"],
                [True, False, False, False, False, True, True],
            ),
            (["root", "C", "c", "D", "e"], [True, False, False, False, True]),
            (
                ["root", "C", "c", "D", "e", "A"],
                [True, False, False, False, True, True],
            ),
            (["root", "C", "c", "E"], [True, False, False, True]),
            (["root", "C", "c", "E", "a"], [True, False, False, True, False]),
            (["root", "C", "c", "E", "b"], [True, False, False, True, False]),
            (["root", "C", "c", "E", "c"], [True, False, False, True, False]),
            (["root", "C", "c", "E", "d"], [True, False, False, True, True]),
            (["root", "C", "d"], [True, False, False]),
            (["root", "C", "e"], [True, False, True]),
            (["root", "D"], [True, True]),
            (["root", "D", "a"], [True, True, False]),
            (["root", "D", "b"], [True, True, False]),
            (["root", "D", "c"], [True, True, False]),
            (["root", "D", "d"], [True, True, False]),
            (["root", "D", "e"], [True, True, True]),
        ]

        rows = Peekable(iter(rows))
        formatted_rows = list(printer._format_row(rows))

        assert formatted_rows == [
            ([""], ["root"]),
            (["", "├──"], ["root", "A"]),
            (["", "├──"], ["root", "B"]),
            (["", "├──"], ["root", "C"]),
            (["", "│  ", "├──"], ["root", "C", "a"]),
            (["", "│  ", "├──"], ["root", "C", "b"]),
            (["", "│  ", "├──"], ["root", "C", "c"]),
            (["", "│  ", "│  ", "├──"], ["root", "C", "c", "A"]),
            (["", "│  ", "│  ", "├──"], ["root", "C", "c", "B"]),
            (["", "│  ", "│  ", "├──"], ["root", "C", "c", "C"]),
            (["", "│  ", "│  ", "├──"], ["root", "C", "c", "D"]),
            (["", "│  ", "│  ", "│  ", "├──"], ["root", "C", "c", "D", "a"]),
            (["", "│  ", "│  ", "│  ", "├──"], ["root", "C", "c", "D", "b"]),
            (["", "│  ", "│  ", "│  ", "├──"], ["root", "C", "c", "D", "c"]),
            (["", "│  ", "│  ", "│  ", "├──"], ["root", "C", "c", "D", "d"]),
            (
                ["", "│  ", "│  ", "│  ", "│  ", "├──"],
                ["root", "C", "c", "D", "d", "A"],
            ),
            (
                ["", "│  ", "│  ", "│  ", "│  ", "├──"],
                ["root", "C", "c", "D", "d", "B"],
            ),
            (
                ["", "│  ", "│  ", "│  ", "│  ", "└──"],
                ["root", "C", "c", "D", "d", "C"],
            ),
            (
                ["", "│  ", "│  ", "│  ", "│  ", "   ", "└──"],
                ["root", "C", "c", "D", "d", "C", "a"],
            ),
            (["", "│  ", "│  ", "│  ", "└──"], ["root", "C", "c", "D", "e"]),
            (
                ["", "│  ", "│  ", "│  ", "   ", "└──"],
                ["root", "C", "c", "D", "e", "A"],
            ),
            (["", "│  ", "│  ", "└──"], ["root", "C", "c", "E"]),
            (["", "│  ", "│  ", "   ", "├──"], ["root", "C", "c", "E", "a"]),
            (["", "│  ", "│  ", "   ", "├──"], ["root", "C", "c", "E", "b"]),
            (["", "│  ", "│  ", "   ", "├──"], ["root", "C", "c", "E", "c"]),
            (["", "│  ", "│  ", "   ", "└──"], ["root", "C", "c", "E", "d"]),
            (["", "│  ", "├──"], ["root", "C", "d"]),
            (["", "│  ", "└──"], ["root", "C", "e"]),
            (["", "└──"], ["root", "D"]),
            (["", "   ", "├──"], ["root", "D", "a"]),
            (["", "   ", "├──"], ["root", "D", "b"]),
            (["", "   ", "├──"], ["root", "D", "c"]),
            (["", "   ", "├──"], ["root", "D", "d"]),
            (["", "   ", "└──"], ["root", "D", "e"]),
        ]


if __name__ == "__main__":
    import pytest

    pytest.main(args=[__file__, "--doctest-modules", "-v", "--capture=sys"])
