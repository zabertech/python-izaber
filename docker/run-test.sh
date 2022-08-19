#!/bin/bash

export PATH="$HOME/.poetry/bin:$PATH"
cd /src
rm -f tests/*.pyc
nox

