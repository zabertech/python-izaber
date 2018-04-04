#!/usr/bin/python

from setuptools import setup

setup(name='izaber',
      version='1.07',
      description='Base load point for iZaber code',
      author='Aki Mimoto',
      url = 'https://github.com/zabertech/python-izaber',
      download_url = 'https://github.com/zabertech/python-izaber/archive/1.7.tar.gz',
      author_email='aki+izaber@zaber.com',
      license='MIT',
      packages=['izaber'],
      scripts=[
        'scripts/izaber-config'
      ],
      install_requires=[
          'PyYAML',
          'pytz',
          'python-dateutil',
          'appdirs',
          'Jinja2',
          'setuptools',
      ],
      zip_safe=False)

