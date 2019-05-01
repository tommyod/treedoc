#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Printers: objects that format rows in the tree.
"""

import inspect
import pydoc
import abc
import collections


class PrinterABC(abc.ABC):
    """Abstract base class for printers."""

    @abc.abstractmethod
    def __init__():
        pass

    @abc.abstractmethod
    def format_row():
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
            # + ("\n\t" + docstring if docstring else "")
        )  # + '\n'
