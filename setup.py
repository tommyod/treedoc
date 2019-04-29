from setuptools import find_packages, setup

setup(
    name="treedoc",
    version="0.0.1",
    description="Minimalistic Python documentation in a tree structure.",
    long_description="Minimalistic Python documentation in a tree structure.",
    author="tommyod",
    author_email="tod001@uib.no",
    license="MIT",
    packages=find_packages(exclude=['*tests*']),
    python_requires=">=3.5",
    install_requires=[],
    # https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    entry_points={"console_scripts": ["treedoc = treedoc.main:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["documentation"],
)
