#!/usr/bin/python

import unittest
import re

from izaber import config, initialize
from izaber.templates import parse
from izaber.email import mailer

class Test(unittest.TestCase):

    def test_email(self):
        parsed = mailer.template_parse(
                      '{{template_path}}/test.email'
                  )
        self.assertTrue(re.search('hello',parsed.as_string()))
        result = mailer.template_send(
                      '{{template_path}}/test.email'
                  )


if __name__ == '__main__':
    initialize(
        name='overlay_test',
        config='data/zaber.yaml'
    )
    unittest.main()


