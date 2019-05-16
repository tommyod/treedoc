#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for printer classes.
"""

import abc
import collections

from treedoc.utils import (
    Peekable,
    clean_object_stack,
    format_signature,
    get_docstring,
    # inspect_classify,
    resolve_str_to_obj,
    describe,
)

from treedoc.utils_meta import PrintMixin


class PrinterABC(abc.ABC):
    """Abstract base class (ABC) for printers."""

    @abc.abstractmethod
    def __init__():
        pass

    @abc.abstractmethod
    def format_iterable():
        """Takes an iterable yielding object stacks and yields formatted strings.
        
        Parameters:
        -----------
        iterator (Iterator): an iterator yielding (print_stack, stack). The stacks
                             are lists representing paths in the object tree.
        
        Yields
        -------
        formatted_str (string) : a string to be printed
        """
        pass


class Printer(PrintMixin):
    """Base class for printers used for input validation."""

    def __init__(
        self, *, signature: int = 1, docstring: int = 2, info: int = 2, width: int = 88
    ):
        """Initialize a printer.
        
        The interpretation of the following arguments varies from printer to printer.
        
        Arguments
        ---------
            signature (int) :  how much signature information to show
            docstring (int) :  how much docstring information to show
            info (int) :  how much general information to show
            width (int) :  maximum character width

        """
        assert signature in (0, 1, 2, 3, 4)
        assert docstring in (0, 1, 2)
        assert info in (0, 1, 2, 3, 4)
        assert width in range(2 ** 6, 2 ** 8 + 1)
        self.signature = signature
        self.docstring = docstring
        self.info = info
        self.width = width

    def _validate_row(self, row):
        assert isinstance(row, collections.abc.Sequence)
        assert len(row) > 0
        assert all((hasattr(obj, "__name__") for obj in row))


class DensePrinter(Printer, PrinterABC):

    SEP = " -> "
    END = "\n"
    SPACES2 = "  "
    SPACES4 = 2 * SPACES2

    def _get_docstring(self, obj) -> str:
        """Get and format docstring from an object."""

        if self.docstring == 0:
            return ""
        return get_docstring(obj, width=self.width)

    def _format_signature(self, obj) -> str:
        """Get and format signature from an object."""
        formatted = format_signature(obj, verbosity=self.signature)
        assert isinstance(formatted, str)
        return formatted

    def format_iterable(self, iterable):

        for stack in self._format_row(iterable):

            self._validate_row(stack)

            # The row represents a path in the tree, the leaf object is the "final" object
            *_, last_obj = stack

            # Attempt to get a signature for the last object
            signature = self._format_signature(last_obj)

            # Get docstring information from the leaf object
            docstring = self._get_docstring(last_obj)

            # Info determines how much to show
            if self.info == 0:
                obj_names = stack[-1].__name__
            else:
                obj_names = ".".join([s.__name__ for s in clean_object_stack(stack)])

            yield (
                "{}|".format(describe(last_obj))
                + self.SPACES2 * len(stack)
                + obj_names
                + signature
                + self.SPACES4
                + docstring
            )

    def _format_row(self, iterable):
        """Yield the object stack from the iterable."""
        for stack, final_node_at_depth in iterable:
            yield stack


class TreePrinter(Printer, PrinterABC):

    # Class attributes used for printing
    RIGHT = "├──"
    DOWN = "│  "
    LAST = "└──"
    BLANK = "   "

    def _get_docstring(self, obj) -> str:
        """Get and format docstring from an object."""

        if self.docstring == 0:
            return ""
        return get_docstring(obj, width=self.width)

    def _format_signature(self, obj) -> str:
        """Get and format signature from an object."""
        formatted = format_signature(obj, verbosity=self.signature)
        assert isinstance(formatted, str)
        return formatted

    def format_iterable(self, iterable):
        # See the Abstract Base Class for the docstring
        # Summary: take an iterable object yielding (stack, final_node_at_depth)
        # and returns strings
        assert isinstance(iterable, collections.abc.Iterable)

        for print_stack, stack in self._format_row(iterable):
            joined_print_stack = " ".join(print_stack)

            # Info determines how much to show
            if self.info == 0:
                obj_names = stack[-1].__name__
            else:
                obj_names = ".".join([s.__name__ for s in clean_object_stack(stack)])

                # TODO: Remove this
                try:
                    resolve_str_to_obj(obj_names)
                except ImportError:
                    pass
                # if resolve_str_to_obj(obj_names) is None:
                #    pass
                # print("FAILED TO LOAD")
                # print(obj_names)
                # assert resolve_str_to_obj(obj_names) is not None

            # TODO: Differentiate between INFO = 1 AND INFO = 2

            last_obj = stack[-1]
            signature = self._format_signature(last_obj)
            docstring = self._get_docstring(last_obj)

            yield " ".join([joined_print_stack, obj_names]) + signature

            # No need to show docstring, or no docstring to show, simply continue
            if self.docstring == 0 or docstring == "":
                continue

            # Want to print with docstring on the new line. Logic to switch up symbols
            last_in_stack = print_stack[-1]
            if last_in_stack == self.RIGHT:
                symbol = self.DOWN
            elif last_in_stack == self.LAST:
                symbol = self.BLANK
            else:
                symbol = ""

            print_stack[-1] = symbol
            yield " ".join([" ".join(print_stack), '"{}"'.format(docstring)])

    def _format_row(self, iterator, depth=0, print_stack=None):
        """Takes an iterator and yields tuples (print_stack, stack).
        
        This recursive generator takes an iterator which yields 
        (stack, final_node_at_depth) and from it computes (print_stack, stack).
        It's purpose is to generate the pretty tree-structure from the 
        `final_node_at_depth` stack."""

        if not isinstance(iterator, Peekable):
            iterator = Peekable(iter(iterator))

        print_stack = print_stack or [""]

        # =============================================================================
        #         BOUNDARY CONDITIONS - For the root node and leaf nodes
        # =============================================================================

        # Peek to see if this is the final note. If it is, return
        stack, final_node_at_depth = iterator.peek((False, False))
        if not stack and not final_node_at_depth:
            return

        # Special case for the root note
        if len(stack) == 1:
            yield print_stack, stack
            next(iterator)
            yield from self._format_row(
                iterator, depth=depth + 1, print_stack=print_stack
            )
            return

        # =============================================================================
        #         ITERATE OVER NODES - Iteration and recursion if needed
        # =============================================================================

        # Iterate over every child at this level
        while True:

            # Get new elements from the iterator, default is (False, False)
            stack, final_node_at_depth = next(iterator, (False, False))

            # We reached the end of the tree, and must go up in the structure
            if not stack and not final_node_at_depth:
                return

            # At the current depth, is this node the final one?
            final_at_depth = final_node_at_depth[depth]

            # Yield the current node at the current depth
            symbol = self.LAST if final_at_depth else self.RIGHT
            yield print_stack + [symbol], stack

            # TODO: IMPORTANT: Calling `peek` will override the `stack` and
            # `final_node_at_depth` variables. I am not sure why.
            # But we need to get all information from these before the `peek` call.
            len_stack = len(stack)

            next_stack, next_final_node_at_depth = iterator.peek((False, False))

            # We reached the end of the tree, and must go up in the structure
            if not next_stack and not next_final_node_at_depth:
                return

            # The next stack has more elements, so it's a child of the current node
            if len(next_stack) > len_stack:

                # Find the appropriate recursion symbol and then recurse
                rec_symbol = self.BLANK if final_at_depth else self.DOWN

                yield from self._format_row(
                    iterator,
                    depth=depth + 1,
                    print_stack=print_stack.copy() + [rec_symbol],
                )

                # The node was the final one at this level, so we go up in the tree
                if final_at_depth:
                    return
            elif len(next_stack) < len_stack:
                # The node was the final one at this level, so we go up in the tree
                return
            else:
                # The next stack is of the same length as the current one
                continue


if __name__ == "__main__":
    import pytest

    pytest.main(args=[".", "--doctest-modules", "-v", "--capture=sys"])
