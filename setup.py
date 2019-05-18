from setuptools import find_packages, setup

setup(
    name="treedoc",
    version="0.2.0",
    description="Minimalistic Python documentation in a tree structure.",
    long_description="Minimalistic Python documentation in a tree structure.",
    author="tommyod",
    author_email="tod001@uib.no",
    license="MIT",
    packages=find_packages(exclude=["*tests*"]),
    python_requires=">=3.6",
    install_requires=[],
    # https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    entry_points={"console_scripts": ["treedoc = treedoc.main:CLI_entrypoint"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords=["documentation"],
)
