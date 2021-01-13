#!/usr/bin/python

from izaber import config, initialize

def test_config():

    # Check that basic configuration options are being respected
    assert config.email.host == 'localhost'
    assert config.email.misc == '127.0.0.1'

    # Checks to see if the overlay is working
    assert config.email.explicit == 'done!'

    # Tests to see if the "config_amend" option is working
    assert config.test.this.thing == 'hi!'

config_amend = """
default:
    test:
        this:
            thing: 'hi!'
"""

initialize(
    name='overlay_test',
    config={
        'config_filename': 'data/izaber.yaml',
        'config_amend': config_amend,
    },
    email={
        'explicit': 'done!'
    }
)
test_config()

