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

    # Try a dot notation get with default default
    assert config.get('test.this.thing') == 'hi!'
    assert config.get('not.this.thing') is None

    # Try a dot notation get miss with explicit default
    assert config.get('test.this.thing', 'nope') == 'hi!'
    assert config.get('not.this.thing', 'nope') == 'nope'

    # Try a non-string key miss
    assert config.get(1, 'nope') == 'nope'

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

