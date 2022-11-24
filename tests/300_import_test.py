from izaber import config, initialize
from izaber.submodule import CHECKS
from izaber_submodule import CHECKS as CHECKS2

# Important! We must load the underscore version of the library
# before the dotted syntax to trigger a load order event
# that we want to test for
from izaber_submodule_subsubmodule import CHECKS as CHECKS4, DATA as DATA2
from izaber.submodule.subsubmodule import CHECKS as CHECKS3, DATA as DATA1

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
    assert CHECKS4['executed'] == 1

    # Are the variables the same?
    CHECKS3['foo'] = 'bar'
    CHECKS4['foo'] = 'baz'
    assert CHECKS3['foo'] == CHECKS4['foo']
    assert CHECKS4['foo'] == 'baz'

    # Are objects the same?
    assert id(DATA1) == id(DATA2)

    # Let's import something that doesn't exist
    try:
        import izaber.nonexistant
    except ModuleNotFoundError:
        pass # this is the error we wish to see

initialize(config='data/izaber.yaml')

test_submodule()

