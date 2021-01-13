#!/bin/bash

export PATH="$HOME/.poetry/bin:$PATH"
cd /python-izaber
poetry install
poetry update

