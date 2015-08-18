#!/usr/bin/python

import unittest

from izaber import config, initialize

class Test(unittest.TestCase):

    def test_config(self):
        self.assertEqual(config.email.host,'localhost')

if __name__ == '__main__':
    initialize(config='data/zaber.yaml')
    unittest.main()

