# izaber


## Overview

This module provides basic functionality that's often reinvented across
many of Zaber's scripts. It provides a unified configuration interface to
allow a single YAML file to hold information that can be used across 
multiple applications as well as generic tools to handle basic services
such as logging, email and templates.

Other modules such as izaber-cron will allow additional services such as
scheduled event and SQL support.

## Documentation

API documentation, usage and examples can be found in the "docs" directory.

## Installation

This library is uploaded to PyPi. Installation for usage can be done with:

`pip install python-izaber`

## Development

For hacking on the code, this requires the following:

- `git`
- `python3`
- [poetry](https://python-poetry.org/)

### Setup

```bash
git clone git@github.com:zabertech/python-izaber.git
cd python-izaber
poetry install
poetry shell
```

And now it's possible to make changes to the code

### Tests via CLI

As we test on multiple versions of python, getting setup for tests is a bit annoying.

Running on Ubuntu, the setup process is to install the appropriate python versions as well as required support binaries and libraries.

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo add-apt-repository ppa:pypy/ppa
sudo apt install pypy3 python3.6 python3.7 python3.8 python3.9 libxml2-dev libxslt1-dev build-essential pypy3-dev python3.6-dev python3.7-dev python3.8-dev python3.9-dev libssl-dev
```

Then running the tests becomes:

```bash
poetry run nox
```

### Tests via Docker

It's not always desireable to pollute the environment with multiple versions of python so a Dockerfile is provided for testing.

```bash
docker build -t tests-izaber .
docker run tests-izaber
```

To use the local copy of the library files, can do the following instead:

```bash
docker run --rm -v `pwd`:/src tests-izaber
```

### Packaging

- Ensure that the `pyproject.toml` has the newest version.
- Update the `VERSIONS.md` with the changes made into the library
- Then, assuming access to the pypi account. [Poetry can publish to PyPI](https://python-poetry.org/docs/libraries/#publishing-to-pypi)
    ```bash
    poetry build
    poetry publish
    ```

