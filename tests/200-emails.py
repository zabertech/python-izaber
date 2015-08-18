#!/usr/bin/python

import unittest

from izaber import config, initialize
from izaber.templates import parse
from izaber.email import mailer

class Test(unittest.TestCase):

    def test_email(self):
        match_str = u"Hello world!"
        result = parse("{{template_path}}/hello.html",test=match_str)
        self.assertEqual(result,match_str)

if __name__ == '__main__':
    initialize(config='data/zaber.yaml')
    unittest.main()


