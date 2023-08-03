#!/usr/bin/python

import unittest

from izaber import config, initialize
from izaber.templates import parse

def test_templates():
    initialize('test',config='data/izaber.yaml')
    match_str = u"Hello world!"
    result = parse("{{template_path}}/hello.html",test=match_str)
    assert result == match_str

if __name__ == "__main__":
    test_templates()

