#!/usr/bin/python

from izaber import config, initialize
from izaber.submodule import CHECKS

def test_submodule():
    assert CHECKS.get('loaded')

initialize(config='data/izaber.yaml')

test_submodule()

