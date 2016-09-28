#!/usr/bin/python

from setuptools import setup

import izaber

setup(name='izaber',
      version=izaber.__version__,
      description='Base load point for iZaber code',
      url='',
      author='Aki Mimoto',
      author_email='aki+izaber@zaber.com',
      license='MIT',
      packages=['izaber'],
      scripts=[
        'scripts/izaber-config'
      ],
      install_requires=[
          'PyYAML',
          'appdirs',
          'Jinja2'
      ],
      zip_safe=False)

