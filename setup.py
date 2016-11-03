#!/usr/bin/python

from setuptools import setup

setup(name='izaber',
      version='1.00',
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

