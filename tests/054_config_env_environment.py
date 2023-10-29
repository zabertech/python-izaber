#!/usr/bin/python

"""
In this test, we verify that we can change the environment from
the default to the `alternate` environment by the `IZABER_ENVIRONMENT`
value
"""

import os
from izaber import config, initialize

ENV_DATA = """
default:
  log:
      level: 50
alternate:
  log:
      level: 10
alternate2:
  log:
      level: 100
"""

def test_config():
    # We're going to define the configuration in the environment
    os.environ['IZABER_YAML'] = ENV_DATA

    # Switch to the `alternate` enviroment
    os.environ['IZABER_ENVIRONMENT'] = 'alternate'

    initialize( force=True )

    # We should see `10` rather than `50`
    assert config.log.level == 10

    # Reload environment using default
    del os.environ['IZABER_ENVIRONMENT']

    initialize( force=True )

    # We should be back to the `default` environment
    assert config.log.level == 50

    # Let's ensure that the explicit load overtakes the
    # environment option
    os.environ['IZABER_ENVIRONMENT'] = 'alternate'
    initialize( force=True, environment='alternate2' )

    # Due to precedence, we should be using the `alternate2`
    # environment
    assert config.log.level == 100

if __name__ == "__main__":
    test_config()

