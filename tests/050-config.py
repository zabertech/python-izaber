#!/usr/bin/python

import unittest

from izaber import config, initialize

class Test(unittest.TestCase):

    def test_config(self):

        # Check that basic configuration options are being respected
        self.assertEqual(config.email.host,'localhost')
        self.assertEqual(config.email.misc,'127.0.0.1')

        # Checks to see if the overlay is working
        self.assertEqual(config.email.explicit,'done!')

        # Tests to see if the "config_amend" option is working
        self.assertEqual(config.test.this.thing,'hi!')

config_amend = """
default:
    test:
        this:
            thing: 'hi!'
"""

if __name__ == '__main__':
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
    unittest.main()

