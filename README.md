# treedoc [![Build Status](https://api.travis-ci.com/tommyod/treedoc.svg?branch=master)](https://travis-ci.com/tommyod/treedoc) [![PyPI version](https://badge.fury.io/py/treedoc.svg)](https://pypi.org/project/treedoc/)  [![Downloads](https://pepy.tech/badge/treedoc)](https://pepy.tech/project/treedoc) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Minimalistic Python documentation in a tree structure.

The `help` command gives much detailed about a single object, while `dir` gives little information about many objects.
The `treedoc` command aims to hit the sweet spot between the two, and you can use it to:
- Explore the Python standard library.
- Get an overview of a package without clicking through dozens of websites.
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

Contributions are very wel
