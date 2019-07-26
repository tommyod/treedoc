# <img src="https://raw.githubusercontent.com/tommyod/treedoc/master/branding/icons/treedoc_white_rounded.png" height="60">
[![Build Status](https://api.travis-ci.com/tommyod/treedoc.svg?branch=master)](https://travis-ci.com/tommyod/treedoc) [![PyPI version](https://badge.fury.io/py/treedoc.svg)](https://pypi.org/project/treedoc/)  [![Downloads](https://pepy.tech/badge/treedoc)](https://pepy.tech/project/treedoc) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Minimalistic Python documentation for dendrophiles.

treedoc prints minimalistic Python documentation in a tree structure,
aiming to hit the sweet spot between detailed information about
a single object and superficial information about object attributes.

treedoc is great for:
- Getting an overview of a package without endlessly scrolling through a website.
- Searching through documentation.
- Printing essential information about different Python objects. 

## Installation

Install from [Python Package Index](https://pypi.org/project/treedoc/) (PyPI) using `pip install treedoc`.

## Usage

treedoc can be used directly through the command-line interface,
or interactively in a Python shell or Jupyter notebook. For more information
about arguments, see `treedoc --help` or `help(treedoc)`.

### Command-line interface

![Example 1 - See the GitHub repo](https://github.com/tommyod/treedoc/blob/master/branding/examples/example_list.gif)

![Example 2 - See the GitHub repo](https://github.com/tommyod/treedoc/blob/master/branding/examples/example_collectionsabc.gif)

![Example 3 - See the GitHub repo](https://github.com/tommyod/treedoc/blob/master/branding/examples/example_pandas_grep.gif)


## Python shell and notebooks

treedoc can be imported and used just like any other package, e.g. in an
interactive Python interpreter session or a Jupyter notebook. 

### Interpreter
![Example 4 - See the GitHub repo](https://github.com/tommyod/treedoc/blob/master/branding/examples/example_python_list.gif)

### Jupyter notebook
![Example 5 - See the GitHub repo](https://github.com/tommyod/treedoc/blob/master/branding/examples/example_jupyter_list.gif)

## Contributing

Contributions are welcome.
If you wish to work on a problem, please create a [pull request](https://github.blog/2019-02-14-introducing-draft-pull-requests/) to get feedback.
We aim for:

- Zero dependencies, but dependencies for testing are ok.
- Idiomatic, clean Python code. Readability matters.
- Thorough testing and code formatting, see `.travis.yml` for commands run by continuous integration.
