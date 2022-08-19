#!/usr/bin/python

from izaber import config, initialize
from izaber.submodule import CHECKS
from izaber_submodule import CHECKS as CHECKS2
from izaber.submodule.subsubmodule import CHECKS as CHECKS3
from izaber_submodule_subsubmodule import CHECKS as CHECKS4

def test_submodule():

    # This validates that izaber_submodules loads
    assert CHECKS2.get('loaded')
    assert CHECKS.get('loaded')
    assert CHECKS == CHECKS2

    # This validates taht izaber_submodules_submodules gets handled as well
    assert CHECKS3.get('loaded')
    assert CHECKS4.get('loaded')
    assert CHECKS3 == CHECKS4
    assert CHECKS3['executed'] == 1

initialize(config='data/izaber.yaml')

test_submodule()

