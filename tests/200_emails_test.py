#!/usr/bin/python

import re

from izaber import config, initialize
from izaber.templates import parse
from izaber.email import mailer

def test_email():
    initialize(
        name='overlay_test',
        config='data/izaber.yaml'
    )

    parsed = mailer.template_parse(
                  '{{template_path}}/test.email'
              )
    assert re.search('test email',parsed.as_string())

    result = mailer.template_send(
                  '{{template_path}}/test.email'
              )


if __name__ == "__main__":
    test_email()

