#!/bin/bash

export PATH="$HOME/.poetry/bin:$PATH"
cd /src
poetry install
poetry update

