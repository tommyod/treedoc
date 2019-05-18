from setuptools import find_packages, setup

setup(
    name="treedoctestpackage",
    version="0.0.1",
    description="A test package for treedoc.",
    long_description="A test package for treedoc.",
    author="tommyod",
    author_email="tod001@uib.no",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[],
    # https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
