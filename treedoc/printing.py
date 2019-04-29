#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Printers: objects that format rows in the tree.
"""

import inspect
import pkgutil
import pydoc

# =============================================================================
# for importer, modname, ispkg in pkgutil.iter_modules(KDEpy.__path__):
#     print(importer, modname, ispkg)
# =============================================================================


def get_modules(package, recurse=False):

    print(package)
    if not hasattr(package, "__path__"):
        return

    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        print(importer, modname, ispkg)
        if ispkg and recurse:
            get_modules(
                importer.find_module(modname).load_module(modname), recurse=recurse
            )







class SimplePrinter:
    
    
    SEP = " -> "
    END = "\n"
    
    def __init__(self, *, signature=1, docstring=1):
        self.signature = 0
        self.docstring = docstring
        
        
    def _get_docstring(self, final_object):
        
        first_line, rest_lines = pydoc.splitdoc(pydoc.getdoc(final_object))
        
        if self.docstring == 0:
            return ''
        elif self.docstring == 1:
            return first_line
        elif self.docstring == 2:
            return first_line
        else:
            pass
        # TODO
        
        
    def _format_argspec(self, final_object):
        
        if self.signature == 0:
            return '()'
        elif self.signature == 1:
            return "(" + ", ".join(inspect.getfullargspec(final_object).args) + ")"
        elif self.signature == 2:
            return "(" + ", ".join(inspect.getfullargspec(final_object).args) + ")"
        else:
            pass
        # TODO

    def print_row(self, row):

        *_, final_object = row
        
        
        try:
            inspect.getfullargspec(final_object)
            signature = self._format_argspec(final_object)
        except TypeError:
            signature = ''
            
            
        docstring = self._get_docstring(final_object)
        
        return (
                self.SEP.join([c.__name__ for c in row])
                + signature
                #+ ("\n\t" + docstring if docstring else "")
            ) #+ '\n'
