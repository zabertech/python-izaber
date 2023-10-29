#!/usr/bin/python

"""
This is a series of tests to verify if we are able to load configuration
data from the environment
"""

import os
from izaber import config, initialize

ENV_DATA = """
default:
  log:
      level: 50
  paths:
      path: './data'
      template_path: '{{path}}/templates'
  email:
      debug: true
      host: localhost
      misc: user
  cron:
      sql:
          default: 'postgresql://scott:tiger@localhost/test'
          rw: 'postgresql://scott:tiger@localhost/test'

"""

def test_config():
    config_amend = """
    default:
        test:
            this:
                thing: 'hi!'
    """

    # We're going to define the configuration in the environment
    os.environ['IZABER_YAML'] = ENV_DATA

    initialize(
        config={
            'config_filename': 'data/izaber-NONEXIST.yaml',
            'config_amend': config_amend,
        },
        email={
            'explicit': 'done!'
        },
        force=True,
    )

    # Check that basic configuration options are being respected
    assert config.email.host == 'localhost'

    # Checks to see if the overlay is working
    assert config.email.explicit == 'done!'

    # Tests to see if the "config_amend" option is working
    assert config.test.this.thing == 'hi!'

    # Try a dot notation get with default default
    assert config.get('test.this.thing') == 'hi!'
    assert config.get('not.this.thing') is None

    # Try a dot notation get miss with explicit default
    assert config.get('test.this.thing', 'nope') == 'hi!'
    assert config.get('not.this.thing', 'nope') == 'nope'

    # Try a non-string key miss
    assert config.get(1, 'nope') == 'nope'


if __name__ == "__main__":
    test_config()

