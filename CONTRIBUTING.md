## Table of contents

- Contributing
- Existing work
- Maintainers

## Contributing

You are very welcome to scrutinize the code and make pull requests if you have suggestions and improvements.
Your submitted code must be PEP8 compliant, and all tests must pass.

If you wish to work on a problem, please create a Work In Progress (WIP) pull request to get feedback.
We aim for:

- Zero dependencies, but dependencies for testing are ok.
- Idiomatic, clean Python code. Readability matters.
- Thorough testing and code formatting, see `.travis.yml` for commands run by continuous integration.

## Existing work

Below is a survey of similar packages and scripts.

- The built-in `dir` function along with [`inspect`](https://docs.python.org/3/library/inspect.html) is of great help
- There's a package in the standard library called [`pydoc`](https://docs.python.org/3/library/pydoc.html)
  - The source is found at [`Lib/pydoc.py](https://github.com/python/cpython/blob/master/Lib/pydoc.py)
- The package [`ljcooke/see`](https://github.com/ljcooke/see) is "Python's dir() for humans."
- The package [`gabrielcnr/python-ls`](https://github.com/gabrielcnr/python-ls) is "Python's dir builtin with recursive search."
- The Sphinx package has functionality we might find interesting, see
  - [`util/inspect.py`](https://github.com/sphinx-doc/sphinx/blob/master/sphinx/util/inspect.py)
  - [`ext/autosummary/generate.py`](https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/autosummary/generate.py)                                                                                                            
  - [`ext/autodoc/__init__.py`](https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/autodoc/__init__.py)
  - [`ext/apidoc.py`](https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/apidoc.py)
- This [`script`](https://gist.github.com/lyoshenka/f9588f273a4840c5a751432af4222517)
- [`vadivelmurugank/inspectshow`](https://github.com/vadivelmurugank/inspectshow)- "inspectshow module lists all the module internals in a tree format."


## Maintainers

### Creating a new release

We use [Semantic Versioning 2.0.0](https://semver.org/).
Pull the latest master branch commit (without creating a merge commit), create a tag, and then push the tag to GitHub.
Make sure that the `__version__` constant corresponds with the git version tag.
Trigger the Travis CI build, which will upload tagged commits to PyPI.

```bash
$ git tag v.X.Y.Z
$ git push origin tag v.X.Y.Z
```
