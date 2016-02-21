Extending
===============================================

Introduction
------------

The basic services provided in iZaber's base library are obviously not enough for a full application. Python also doesn't like to share the namespace into submodules without a bit of work.

This document is to describe how to create modules under the namespace "izaber" and link that code to existing izaber services.

Basic Concepts
--------------

When an import is performed, usually python expects to find corresponding to the import.

It's actually possible to override the import behaviour and the details can be found in izaber/__init__.py.

To extend the iZaber library so that it's possible to create submodules we abuse this facility quite liberally.

That takes care of the namespace but there is also the issue of initialization of mutiple modules (connecting to servers, cache prep, etc) so there also exists ways to organize the initialiation sequence as well.

Simple Example: Hello World
---------------------------

To start off, a simple example: "Hello World". All this does is provide a method that prints "Hello World".

This module should be accessible via "izaber.hello". To do so, a new module must be made with the package name "izaber_hello" (removing the period).

The file structure would look like this:

    izaber_hello/
              __init__.py


In the __init__.py file, the code would look like this:

    def greetings():
        print "Hello World"

If the izaber_hello path is in an importable location, using the module would work like this:

  #!/usr/bin/python

  import izaber.hello
  izaber.hello.greetings()

Useful Example: Flask Microframework
------------------------------------

This example creates the module "``izaber.flask``" and will roll in support for using the configuration and existing izaber services.

First the user configuration in "``izaber.yaml``" will include a new keypair ``flask.port`` which will dictate which port flask should start on:

  default:
    debug: true
    log:
        level: 10
    flask:
        port: 8090
    email:
        host: mail.example.com
        from: automatedsender@example.com
        to: recipient@example.com
    paths:
        path: ~

Then a new module is created:

  izaber_flask/
            __init__.py

Let's say, for example, the following example code would be desireable:

  from izaber import initialize
  from izaber.flask import Flask
  app = Flask(__name__)

  @app.route('/')
  def hello_world():
      return 'Hello World!'

  if __name__ == '__main__':
      initialize('example')
      app.run()

To be able to do this, the file izaber_flask/__init__.py would look something like this:

  # Import the configuration variable we'll use to identify the port
  from izaber import config

  # izaber.startup contains code to register and organize initialization calls
  from izaber.startup import initializer

  import flask

  class Flask(flask.Flask):
      def run(self, host=None, port=None, debug=None, **options)
          # If port has not been set, use the default found in the
          # izaber.yaml file
          if port is None:
              port = config.flask.port
          super(self,Flask).run(self,host,port,debug,**options)

  @initializer('flask')
  def initialize(**kwargs):
      # Ensure that the config gets loaded before we do
      request_initialize('config',**kwargs)

This code ensures that the configuration module get initialized before the flask module and by the time ``def run`` is called, that the configuration values are present.

Useful Example: Command Line Configuration Overrides
----------------------------------------------------

In most applications, it would be nice to be able to switch between different configuration overlays at invocation rather than in the code.

In this example, the code will use docopt to parse the command line and select which configuration overlay to use. While this might be a practical example, use izaber_cli instead in practice since it will have greater robustness and features to offer.

The filestructure may look like this:

    izaber_docopt/
              __init__.py

To use this module, the example could could be like this:

  from izaber import initialize
  from izaber.docopt import arguments

  if __name__ == '__main__':
      initialize('example')
      print arguements

Then in the izaber_docopt/__init__.py module, it would be possible to do:

# Import the configuration variable we'll use to identify the port
from izaber import config

# izaber.startup contains code to register and organize initialization calls
from izaber.startup import initializer

arguments = None

@initializer('docopt',before='config')
def initialize(**kwargs):
    pass

