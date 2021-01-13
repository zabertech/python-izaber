#!/usr/bin/python

import unittest

from izaber import config, initialize
from izaber.templates import parse

def test_templates():
    match_str = u"Hello world!"
    result = parse("{{template_path}}/hello.html",test=match_str)
    assert result == match_str

initialize('test',config='data/izaber.yaml')
test_templates()

