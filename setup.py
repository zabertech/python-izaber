from setuptools import setup

setup(name='izaber',
      version='1.0',
      description='Base load point for iZaber code',
      url='',
      author='Aki Mimoto',
      author_email='aki+izaber@zaber.com',
      license='MIT',
      packages=['izaber'],
      install_requires=[
          'PyYAML',
          'appdirs',
          'Jinja2'
      ],
      zip_safe=False)

