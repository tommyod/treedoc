#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Printers: objects that format rows in the tree.
"""

import abc
import collections
import inspect
import pydoc
import copy

from treedoc.utils import inspect_classify, peekable


class PrinterABC(abc.ABC):
    """Abstract base class for printers."""

    @abc.abstractmethod
    def __init__():
        pass

    @abc.abstractmethod
    def format_iterable():
        """
        Format a row, i.e. a path in the tree.
        
        Parameters:
        -----------
        row (Sequence): typically a list with objects, each having the __name__ attr
        
        Returns
        -------
        output (string) : a string for printer, or None if something went wrong
        """
        pass


class Printer:
    """Base class for printers used for input validation."""

    def __init__(self, *, signature=1, docstring=2, info=2):
        """
        Initialize a printer.
        """
        assert signature in (0, 1, 2)
        assert docstring in (0, 1, 2, 3, 4)
        assert info in (0, 1, 2, 3, 4)
        self.signature = signature
        self.docstring = docstring
        self.info = info

    def _validate_row(self, row):
        assert isinstance(row, collections.abc.Sequence)
        assert len(row) > 0
        assert all((hasattr(obj, "__name__") for obj in row))


class SimplePrinter(Printer, PrinterABC):

    SEP = " -> "
    END = "\n"

    def _get_docstring(self, leaf_object):
        """Get and format docstring from the leaf object in the tree path."""

        first_line, rest_lines = pydoc.splitdoc(pydoc.getdoc(leaf_object))

        if self.docstring == 0:
            return ""
        elif self.docstring == 1:
            return first_line
        elif self.docstring == 2:
            return first_line
        else:
            pass
        # TODO: Add more options here

    def _format_argspec(self, leaf_object):
        """Get and format argspec from the leaf object in the tree path."""

        if self.signature == 0:
            return "()"
        elif self.signature == 1:
            return "(" + ", ".join(inspect.getfullargspec(leaf_object).args) + ")"
        elif self.signature == 2:
            return "(" + ", ".join(inspect.getfullargspec(leaf_object).args) + ")"
        else:
            pass
        # TODO: Add more options here

    def format_iterable(self, iterable):

        for stack, final_node_at_depth in iterable:
            yield self.format_row(stack)

    def format_row(self, row):
        # No docstring here, it's inherited from the method PrinterABC.print_row.
        self._validate_row(row)

        # The row represents a path in the tree, the leaf object is the "final" object
        *_, leaf_object = row

        # Attempt to get a signature for the leaf object
        try:
            inspect.getfullargspec(leaf_object)
            signature = self._format_argspec(leaf_object)
        except TypeError:
            signature = ""

        # Get docstring information from the leaf object
        docstring = self._get_docstring(leaf_object)
        docstring = docstring

        return (
            self.SEP.join([c.__name__ for c in row])
            + signature
            + str(inspect_classify(leaf_object))
            # + ("\n\t" + docstring if docstring else "")
        )  # + '\n'


class TreePrinter(Printer, PrinterABC):

    RIGHT = "├──"
    DOWN = "│  "
    LAST = "└──"
    BLANK = "   "

    def _get_docstring(self, leaf_object):
        """Get and format docstring from the leaf object in the tree path."""

        first_line, rest_lines = pydoc.splitdoc(pydoc.getdoc(leaf_object))

        if self.docstring == 0:
            return ""
        elif self.docstring == 1:
            return first_line
        elif self.docstring == 2:
            return first_line
        else:
            pass
        # TODO: Add more options here

    def _format_argspec(self, leaf_object):
        """Get and format argspec from the leaf object in the tree path."""

        if self.signature == 0:
            return "()"
        elif self.signature == 1:
            return "(" + ", ".join(inspect.getfullargspec(leaf_object).args) + ")"
        elif self.signature == 2:
            return "(" + ", ".join(inspect.getfullargspec(leaf_object).args) + ")"
        else:
            pass
        # TODO: Add more options here

    def format_iterable(self, iterable):

        iterable = peekable(iter(iterable))

        for print_stack, stack in self._format_row(iterable, depth=0, print_stack=None):
            joined_print_stack = " ".join(print_stack)
            obj_names = ".".join([s.__name__ for s in stack])
            yield " ".join([joined_print_stack, obj_names])

    def _format_row(self, iterator, depth=0, print_stack=None):
        """Print a row."""

        if not isinstance(iterator, peekable):
            raise TypeError("The iterator must be peekable.")
        iterator = iter(iterator)
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

    import subprocess

    subprocess.call(["treedoc", "list"])
    subprocess.call(["treedoc", "collections"])
    subprocess.call(["treedoc", "pandas"])

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
        (["root", "C", "c", "D", "d", "A"], [True, False, False, False, False, False]),
        (["root", "C", "c", "D", "d", "B"], [True, False, False, False, False, False]),
        (["root", "C", "c", "D", "d", "C"], [True, False, False, False, False, True]),
        (
            ["root", "C", "c", "D", "d", "C", "a"],
            [True, False, False, False, False, True, True],
        ),
        (["root", "C", "c", "D", "e"], [True, False, False, False, True]),
        (["root", "C", "c", "D", "e", "A"], [True, False, False, False, True, True]),
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

    assert all((len(i) == len(j) for i, j in rows))

    RIGHT = "├──"
    DOWN = "│  "
    LAST = "└──"
    BLANK = "   "

    def prow(iterator, depth=0, print_stack=None):
        """Print a row."""

        # =============================================================================
        #         BOUNDARY CONDITIONS - For the root node and leaf nodes
        # =============================================================================

        print_stack = print_stack or [""]

        # print(f"log: prow(iterator, depth={depth}, print_stack={print_stack})")

        # Peek to see if this is the final note. If it is, return
        stack, final_node_at_depth = iterator.peek((False, False))
        if not stack and not final_node_at_depth:
            return

        # Special case for the root note
        if len(stack) == 1:
            print(stack[0])
            next(iterator)
            prow(iterator, depth=depth + 1, print_stack=print_stack)
            return

        # =============================================================================
        #         ITERATE OVER NODES - Iteration and recursion if needed
        # =============================================================================

        # Iterate over every child at this level
        while True:

            stack, final_node_at_depth = next(iterator, (False, False))
            if not stack and not final_node_at_depth:
                # print('End of graph, going up in the structure')
                return

            # print(f"Popped ({stack}, {final_node_at_depth}) at depth {depth}")
            *_, last = stack

            symbol = LAST if final_node_at_depth[depth] else RIGHT
            print(" ".join(print_stack + [symbol]), last)

            next_stack, next_final_node_at_depth = iterator.peek((False, False))
            if not next_stack and not next_final_node_at_depth:
                # print('End of graph, going up in the structure')
                return

            if len(next_stack) > len(stack):
                # print('log: different lengths - we recurse')

                # print_stack.append(rec_symbol)
                rec_symbol = BLANK if final_node_at_depth[depth] else DOWN
                prow(
                    iterator,
                    depth=depth + 1,
                    print_stack=print_stack.copy() + [rec_symbol],
                )

                # print(f'popped print stack: {print_stack}')
                if final_node_at_depth[depth]:
                    break
            elif len(next_stack) < len(stack):
                # print(f'popped print stack: {print_stack}')
                break
            else:
                # print('log: we do not recurse')
                continue

        # print(f"finished: prow(iterator, depth={depth}, print_stack={print_stack})")
        # print_stack.pop()

    from more_itertools import peekable

    iterator = peekable(iter(rows))

    prow(iterator)
