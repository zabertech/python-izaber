#!/bin/bash

export PATH="$HOME/.poetry/bin:$PATH"
cd /python-izaber
rm -f tests/*.pyc
poetry run tox

