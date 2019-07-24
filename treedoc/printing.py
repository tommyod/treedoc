#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for printers (classes) and associated functions.
"""

import abc
import collections
import importlib
import inspect
import os
import pkgutil
import pydoc
import sys
import textwrap
import typing

from treedoc.utils import Peekable, PrintMixin

# =============================================================================
# ------------------------ PART 1/2 OF MODULE - CLASSES -----------------------
# =============================================================================


class PrinterABC(abc.ABC):
    """Abstract base class (ABC) for printers."""

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def format_iterable(self, iterable) -> typing.Generator[str, None, None]:
        """Consumes an iterator yielding object stacks and yields formatted strings.
        
        Parameters
        ----------
        iterator : Iterator
            An iterator yielding (print_stack, stack). 
            The stacks are lists representing paths in the object tree.
        
        Yields
        ------
        formatted_str : string
            A string to be printed
        """
        pass


class Printer(PrintMixin):
    """Base class for printers, used for input validation."""

    def __init__(
        self, *, signature: int = 1, docstring: int = 2, info: int = 2, width: int = 88
    ):
        """Initialize a printer.
        
        The interpretation of the following arguments varies from printer to printer.
        
        Parameters
        ----------
            signature : int
                How much signature information to show
            docstring : int
                How much docstring information to show
            info : int
                How much general information to show
            width : int
                Maximum character width

        """
        assert signature in (0, 1, 2, 3, 4)
        assert docstring in (0, 1, 2)
        assert info in (0, 1, 2, 3, 4)
        assert width in range(2 ** 6, 2 ** 8 + 1)
        self.signature = signature
        self.docstring = docstring
        self.info = info
        self.width = width

    def _validate_obj_stack(self, stack) -> None:
        assert isinstance(stack, collections.abc.Sequence)
        assert len(stack) > 0
        assert all((hasattr(obj, "__name__") for obj in stack))


class DensePrinter(Printer, PrinterABC):

    SEP = " -> "
    END = "\n"
    SPACES2 = "  "
    SPACES4 = 2 * SPACES2

    def _get_docstring(self, obj) -> str:
        """Get and format the docstring of an object."""
        if self.docstring == 0:
            return ""
        return get_docstring(obj, width=self.width)

    def _format_signature(self, obj) -> str:
        """Get and format the signature of an object."""
        formatted = format_signature(obj, verbosity=self.signature, width=self.width)
        assert isinstance(formatted, (str,))
        return formatted

    def format_iterable(self, iterable) -> typing.Generator[str, None, None]:
        """ See the Abstract Base Class for the docstring.
        
        Summary
        -------
        Take an iterable object yielding (stack, final_node_at_depth) and returns strings.
        """
        for stack in self._format_row(iterable):

            self._validate_obj_stack(stack)

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

    def _get_docstring(self, obj, *, width) -> str:
        """Get and format the docstring of an object."""
        if self.docstring == 0:
            return ""

        return get_docstring(obj, width=width)

    def _format_signature(self, obj, *, width) -> str:
        """Get and format the signature of an object."""
        formatted = format_signature(obj, verbosity=self.signature, width=width)
        assert isinstance(formatted, str)
        return formatted

    def format_iterable(self, iterable) -> typing.Generator[str, None, None]:
        """ See the Abstract Base Class for the docstring.
        
        Summary
        -------
        Take an iterable object yielding (stack, final_node_at_depth) and returns strings.
        """
        assert isinstance(iterable, collections.abc.Iterable)

        for print_stack, stack in self._format_row(iterable):

            self._validate_obj_stack(stack)

            joined_print_stack = " ".join(print_stack)

            # Info determines how much to show
            if self.info == 0:
                obj_names = stack[-1].__name__
            else:
                obj_names = ".".join([s.__name__ for s in clean_object_stack(stack)])

            # TODO: Consider a check of whether the object can be resolved here

            # TODO: Differentiate between INFO = 1 AND INFO = 2

            # The 1 represents the spacing between the stacks
            # The 3 represents space and quotation marks in "docstring"
            width_used = len(joined_print_stack) + len(obj_names) + 1

            last_obj = stack[-1]
            signature = self._format_signature(last_obj, width=self.width - width_used)
            docstring = self._get_docstring(
                last_obj, width=self.width - len(joined_print_stack) - 3
            )

            to_yield = " ".join([joined_print_stack, obj_names]) + signature
            assert len(to_yield) <= self.width

            yield to_yield

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
            to_yield = " ".join([" ".join(print_stack), '"{}"'.format(docstring)])
            assert len(to_yield) <= self.width

            yield to_yield

    def _format_row(self, iterator, depth=0, print_stack=None):
        """Takes an iterator and yields tuples (print_stack, stack).
        
        This recursive generator takes an iterator which yields 
        (stack, final_node_at_depth) and from it computes (print_stack, stack).
        It's purpose is to generate the pretty tree-structure from the 
        `final_node_at_depth` stack.
        """

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


# =============================================================================
# ------------------------ PART 2/2 OF MODULE - FUNCTIONS ---------------------
# =============================================================================


def _describe(obj) -> str:
    """Produce a short description of the given object.
    
    Inspired by pydoc.describe.
    """
    if inspect.ismodule(obj):

        if obj.__name__ in sys.builtin_module_names:
            return "built-in module"

        if hasattr(obj, "__path__"):
            return "package"
        else:
            return "module"

    if inspect.isbuiltin(obj):
        return "built-in function"

    if inspect.isgetsetdescriptor(obj):
        return "getset descriptor"

    if inspect.ismemberdescriptor(obj):
        return "member descriptor"

    if inspect.isclass(obj):
        return "class"

    if inspect.isfunction(obj):
        return "function"

    if inspect.ismethod(obj):
        return "method"

    return type(obj).__name__


def describe(obj) -> str:
    """Produce a short description of the given object."""
    return _describe(obj).ljust(17)


def get_docstring(obj, *, width=88) -> str:
    """Get a docstring summary from an object.
    
    If no docstring is available, an empty string is returned.
    
    Examples
    --------
    >>> get_docstring(set.intersection)
    'Return the intersection of two sets as a new set.'
    >>> get_docstring(set.intersection, width=18)
    'Return the...'
    """

    # =============================================================================
    #     TODO: This function needs to become smarter, i.e. more adaptible to
    #     how docstrings are written "in the wild".
    # =============================================================================

    # pydoc.getdoc is slightly more general than inspect.getdoc,see:
    # https://github.com/python/cpython/blob/master/Lib/pydoc.py#L92
    doc = pydoc.getdoc(obj)
    first_line, rest = pydoc.splitdoc(doc)

    # Could not get a single synopsis. Can we get the first two sentences?
    if (not first_line) and rest and ("\n\n" in rest):
        first_line = rest.split("\n\n")[0].replace("\n", " ")

    return_str = textwrap.shorten(first_line, width=width, placeholder="...")

    if return_str:
        return_str = return_str[:-3] if return_str.endswith("....") else return_str
        return return_str

    # If the docstring is a long paragraph, pydoc.splitdoc will return ''
    # We change this behavior to include the start of the string.
    if not return_str and doc:
        return_str = textwrap.shorten(doc, width=width, placeholder="...")
        return_str = return_str[:-3] if return_str.endswith("....") else return_str
        return return_str

    return ""


def clean_object_stack(stack):
    """
    Join an object stack so that consecutive modules are merged into the last one.
    
    This avoids the stack [collections, collections.abc] as being named
    'collections.collections.abc'.
    
    >>> import collections
    >>> from collections import abc
    >>> clean_object_stack([collections, abc]) == [abc]
    True
    >>> from collections import Counter
    >>> input_stack = [collections, Counter, Counter.most_common]
    >>> clean_object_stack(input_stack) == input_stack
    True
    """
    assert isinstance(stack, list)

    stack = stack.copy()
    new_stack = []

    for obj in stack:
        # This one is a module, and the last one is a module
        # Therefore it must be a submodule, get rid of the first one
        # to avoid [collections, collections.abc]
        if new_stack and inspect.ismodule(obj) and inspect.ismodule(new_stack[-1]):
            new_stack.pop()
        new_stack.append(obj)

    assert len(new_stack) > 0
    return new_stack


def _get_name(param) -> str:
    """Checks if signature.Parameter corresponds to *args or **kwargs type input."""
    if (
        param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD)
        and param.default is param.empty
    ):
        return str(param)
    else:
        return param.name


def _between(string, start, end) -> str:
    """Returns what's between `start` and `end`, exclusive.
    
    Examples
    >>> _between("im a nice (person) to all", "(", ")")
    'person'
    >>> _between("im a nice (person to all", "(", ")")
    Traceback (most recent call last):
        ...
    ValueError: substring not found
    """
    i = string.index(start)
    part = string[i + len(start) :]
    j = part.index(")")
    return part[:j]


def signature_from_docstring(obj):
    """Extract signature from built-in object docstring.
    
    Some of the built-in methods have signature info in the docstring. One example is
    `dict.pop`. This method will retrieve the docstring, and return None if it cannot.
    
    >>> import math
    >>> signature_from_docstring(math.log) in ('x[, base]', 'x, [base=math.e]')
    True
    >>> signature_from_docstring(dict.pop) in ('k[,d]', None)
    True
    """

    # If not docstring is available, return
    docstring_line = get_docstring(obj)

    if not docstring_line:
        return None

    # If it's not callable, return
    if not isinstance(obj, collections.abc.Callable):
        return None

    # Look for the name of the object, i.e. func(x)
    assert hasattr(obj, "__name__")

    if not obj.__name__ in docstring_line:
        return None

    # Attempt to get the signature
    index = docstring_line.index(obj.__name__) + len(obj.__name__)
    signature_part = docstring_line[index:]

    try:
        ret_value = _between(signature_part, "(", ")")
        if ret_value:
            return ret_value
    except ValueError:
        return None

    return None


def format_signature(obj, *, verbosity=2, width=88) -> str:
    """ 
    Format a function signature for printing.
    
    This function tries first to use inspect.signature, if that fails it will look for
    signature information in the first line of the docstring, and if that fails it will
    return a generic sigature if the object is callable.
    
    Examples
    --------
    >>> import collections
    >>> # Works on functions with well-defined signature
    >>> format_signature(collections.defaultdict.fromkeys, verbosity=2)
    '(iterable, value)'
    >>> # Built-ins with signature information in the docs
    >>> format_signature(collections.defaultdict.update, verbosity=2)
    '([E, ]**F)'
    >>> # Built-ins with signature no signature information at all
    >>> format_signature(collections.deque.append, verbosity=2)
    '(...)'
    """
    signature_string = _format_signature(obj=obj, verbosity=verbosity)
    assert isinstance(signature_string, str)

    # No problems with the width
    if len(signature_string) <= width:
        return signature_string

    # It's too wide, shorten it and return
    inner_sig = str(signature_string).strip("()")

    try:
        inner_sig = textwrap.shorten(inner_sig, width=width - 2, placeholder=" ...")
    except ValueError:  # ValueError: placeholder too large for max width
        inner_sig = ""

    result = "(" + inner_sig + ")"

    assert len(result) <= width

    return result


def _format_signature(obj, *, verbosity=2) -> str:
    """Format the signature, but make no guarantee for width."""
    # TODO: Figure out how to handle *

    max_verbosity = 4
    assert 0 <= verbosity <= max_verbosity
    SEP = ", "

    # Return formatted signature based on verbosity
    if verbosity == 0:
        return ""

    # Check if object has signature
    try:
        sig = inspect.signature(obj)
    except ValueError:
        # inspect.signature raises ValueError if no signature can be provided.
        # Example:
        # -------
        # >>> inspect.signature(math.log)
        # 'ValueError: no signature found for builtin <built-in function log>'

        signature_in_docs = signature_from_docstring(obj)

        # Failed to find a signature in the docstring
        if signature_in_docs is None:
            # inspect.signature and docstring info has failed, still return if callable
            if callable(obj) and verbosity >= 1:
                return "(...)"
            return ""
        # Found a signature in the docstring
        else:
            if verbosity == 1:
                return "(...)"
            else:
                # TODO: Format this more depending on verbosity
                return "(" + signature_in_docs + ")"
        return ""

    except TypeError:
        # inspect.signature raises TypeError if type of object is not supported.
        # Example:
        # -------
        # >>> x = 1
        # >>> inspect.signature(x)
        # 'TypeError: 1 is not a callable object'
        return ""

    # =============================================================================
    #     If the code reaches this point, we have a Signature stored in `sig`
    # =============================================================================

    # If function as no arguments, return
    if str(sig) == "()" and verbosity > 0:
        return str(sig)

    # Check if signature has annotations or defaults
    annotated = any(
        param.annotation is not param.empty for param in sig.parameters.values()
    )
    has_defaults = any(
        param.default is not param.empty for param in sig.parameters.values()
    )

    # Dial down verbosity if user has provided a more verbose alternative than is available
    if not annotated:
        max_verbosity = 3

    if not has_defaults and not annotated:
        max_verbosity = 2

    if verbosity > max_verbosity:
        # TODO: Give user warning if verbosity needs to be adjusted, e.g.
        # print(f'Adjusting verbosity: {verbosity} -> {max_verbosity}.')
        verbosity = max_verbosity
        # Fails for instance on collections.ChainMap without this logic
        return str(sig)

    elif verbosity == 1:
        return "(...)"

    elif verbosity == 2:
        return_sig = SEP.join(_get_name(param) for param in sig.parameters.values())
        return "(" + return_sig + ")"

    elif verbosity == 3:
        return_sig = SEP.join(
            param.name + "=" + str(param.default)
            if param.default is not param.empty
            else _get_name(param)
            for param in sig.parameters.values()
        )
        return "(" + return_sig + ")"

    else:
        return str(sig)


def resolve_str_to_obj(object_string: str) -> object:
    """
    Resolve a string to a Python object.
    
    list -> builtin
    collections -> module
    collections.Counter -> object
    
    Examples
    --------
    >>> resolve_str_to_obj("list") == list
    True
    >>> import collections
    >>> resolve_str_to_obj("collections") == collections
    True
    >>> from collections import Counter
    >>> resolve_str_to_obj("collections.Counter") == Counter
    True
    >>> resolve_str_to_obj("gibberish.Counter")
    Traceback (most recent call last):
        ...
    ModuleNotFoundError: No module named 'gibberish'
    """
    assert isinstance(object_string, str)

    # Case 1: Some jokster passed the string "None", so we return None back
    if object_string == "None":
        return None

    # Case 2: The object string is "collections.deque" or some dotted path
    suggestion = pydoc.locate(object_string)
    if suggestion is not None:
        return suggestion

    # Case 3: The object string is "myfile.py", i.e. a module
    if object_string.endswith(".py"):
        try:
            # Try to import the file directly, e.g.:
            # /home/username/pythonfiles/functions.py
            return pydoc.importfile(object_string)
        except FileNotFoundError:
            # Join with the current working directory and try
            possible_module = os.path.join(os.getcwd(), object_string)
            return pydoc.importfile(possible_module)

    # Case 4: The object string is "package", a directory with for instance
    # `__init__.py` and `functions.py` under it

    # Must join and split in case user passer "folder/folder/package"
    possible_pkg = os.path.join(os.getcwd(), object_string)
    base, package = os.path.split(os.path.realpath(possible_pkg))

    # Append the base to the system path and try to import the module
    # This allows `__init__.py` in "package" to have imports such as
    # from .functions import func
    # from functions import func
    # and we'll be able to get them. There are probably limits to this hack.
    sys.path.append(base)
    sys.path.append(package)

    try:
        return importlib.import_module(package)
    except:
        sys.path.pop()  # Clean up
        sys.path.pop()
        raise


def resolve_input(obj):
    """Resolve a general input (str, iterable, etc) to a list of Python objects.
    
    Examples
    --------
    >>> resolve_input("list") == [list]
    True
    >>> resolve_input("list dict") == [list, dict]
    True
    >>> len(resolve_input(["python"])) > 10
    True
    >>> resolve_input(["list"]) == [list]
    True
    >>> resolve_input(["list", "dict"]) == [list, dict]
    True
    >>> resolve_input(list) == [list]
    True
    >>> from collections.abc import Collection
    >>> resolve_input("collections.abc.Collection") == [Collection]
    True
    """
    if isinstance(obj, str):
        obj = obj.strip()

    if isinstance(obj, str) and " " in obj:
        # Parse "dict   str  " correctly, ignoring extra whitespace
        obj = [o for o in obj.split(" ") if o != ""]

    # Special handling if "python" is passed
    if isinstance(obj, list) and len(obj) == 1 and obj[0].lower().strip() == "python":
        objects = []
        for (importer, object_name, ispkg) in pkgutil.iter_modules():
            if not ispkg:
                continue
            try:
                obj = importlib.import_module(object_name)
            except:
                continue
            objects.append(obj)
        return objects
    elif isinstance(obj, str):
        assert " " not in obj
        return [resolve_str_to_obj(obj)]
    elif isinstance(obj, (list, set, tuple)):
        attempt = [resolve_str_to_obj(o) if isinstance(o, str) else o for o in obj]
        return [obj for obj in attempt if obj is not None]
    else:
        return [obj]

    raise ValueError("Could not resolve object")


if __name__ == "__main__":
    import pytest

    pytest.main(args=[".", "--doctest-modules", "-v", "--capture=sys"])
