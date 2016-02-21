#!/usr/bin/python

import unittest

from izaber import config, initialize

class Test(unittest.TestCase):

    def test_config(self):
        self.assertEqual(config.email.host,'localhost')
        self.assertEqual(config.email.misc,'127.0.0.1')
        self.assertEqual(config.email.explicit,'done!')

if __name__ == '__main__':
    initialize(
        name='overlay_test',
        config='data/izaber.yaml',
        email={
            'explicit': 'done!'
        }
    )
    unittest.main()

