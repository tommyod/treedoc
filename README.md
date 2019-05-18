# <img src="https://github.com/tommyod/treedoc/branding/icons/treedoc_white_rounded.png" height="48"> [![Build Status](https://api.travis-ci.com/tommyod/treedoc.svg?branch=master)](https://travis-ci.com/tommyod/treedoc) [![PyPI version](https://badge.fury.io/py/treedoc.svg)](https://pypi.org/project/treedoc/)  [![Downloads](https://pepy.tech/badge/treedoc)](https://pepy.tech/project/treedoc) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Minimalistic Python documentation for dendrophiles.

`treedoc` prints minimalistic Python documentation in a tree structure,
aiming to hit the sweet spot between detailed information about
a single object and superficial information about object attributes.

`treedoc` is great for:
- Getting an overview of a package without endlessly scrolling through a website.
- Searching through documentation.
- Printing essential information about different Python objects. 

## Installation

Install from [Python Package Index](https://pypi.org/project/treedoc/) (PyPI) using `pip install treedoc`.

## Usage

`treedoc` provides a simple, efficient and interactive interface to Python
documentation.

### Command-line interface

TODO: Add sentence about GIF below.
![Example
1](https://github.com/tommyod/treedoc/branding/examples/example_list.gif)

TODO: Add sentence about GIF below.
![Example
2](https://github.com/tommyod/treedoc/branding/examples/example_collectionsabc.gif)

TODO: Add sentence about GIF below.
![Example
3](https://github.com/tommyod/treedoc/branding/examples/example_pandas_grep.gif)


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
