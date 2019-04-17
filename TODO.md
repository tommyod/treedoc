# TODO

## What has been done?

- The builtin `dir` function along with [`inspect`](https://docs.python.org/3/library/inspect.html)] is of great help
- There's a package in the standard library called [`pydoc`](https://docs.python.org/3/library/pydoc.html)
- The package [`ljcooke/see`](https://github.com/ljcooke/see) is "Python's dir() for humans."
- The Sphinx package has functionality we might find interesting, see 
  - [`util/inspect.py`](https://github.com/sphinx-doc/sphinx/blob/master/sphinx/util/inspect.py)
  - [`ext/autosummary/generate.py`](https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/autosummary/generate.py)                                                                                                            
  - [`ext/autodoc/__init__.py`](https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/autodoc/__init__.py)
  - [`ext/apidoc.py`](https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/apidoc.py)


## What should we do?

Determine how to structure the software. E.g. we can separate a Module traverser/tree structure, and the printing of it.

- [ ] Setup project structure (we can use cookiecutter)
  - [ ] Testing 
  - [ ] Travis CI 
  - [ ] Pypi stuff 
- [ ] Module traverser
  - [ ] How to determine what an object is 
  - [ ] How to retrieve documentation from an object 
  - [ ] How to store results 
  - [ ] Setup 
- [ ] Printers
  - [ ] Determine which options we want
