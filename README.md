# treedoc [![Build Status](https://api.travis-ci.com/tommyod/treedoc.svg?branch=master)](https://travis-ci.com/tommyod/treedoc) [![PyPI version](https://badge.fury.io/py/treedoc.svg)](https://pypi.org/project/treedoc/)  [![Downloads](https://pepy.tech/badge/treedoc)](https://pepy.tech/project/treedoc) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Minimalistic Python documentation in a tree structure.

```bash
$ treedoc collections
collections
 ├── collections.ChainMap(self)
 │   ├── collections.ChainMap.copy(self)
 │   ├── collections.ChainMap.clear(self)
 │   ├── collections.ChainMap.copy(self)
 │   ├── collections.ChainMap.fromkeys(cls, iterable)
<142 lines omitted>
```

The built-in`help` command gives detailed information about a single object, while `dir` gives superficial information about object attributes.
`treedoc` aims to hit the sweet spot between the two, and is great for:
- Exploring the Python standard library.
- Getting an overview of a package without clicking through a website.
- Perform searches and output minimalistic documentation.

## Installation

Install from [Python Package Index](https://pypi.org/project/treedoc/) (PyPI) using `pip install treedoc`.

## Examples

### Command-line interface

```bash
$ # Information about a built-in
$ treedoc list
$ # Information about EVERY built-in
$ treedoc builtins
$ # Information about a package
$ treedoc collections
$ # Full list of arguments
$ treedoc --help
```

## Python package

```python
>>> from treedoc import treedoc
>>> treedoc(list)
>>> import functools
>>> treedoc(functools)
```

## Contributing

Contributions are welcome.
If you wish to work on a problem, please create a Work In Progress (WIP) pull request to get feedback.
We aim for:

- Zero dependencies, but dependencies for testing are ok.
- Idiomatic, clean Python code. Readability matters.
- Thorough testing and code formatting, see `.travis.yml` for commands run by continuous integration.
