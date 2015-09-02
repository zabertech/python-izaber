Tutorial
===============================================

Introduction
------------

The iZaber base library provides:

* **Configuration:** Unified configuration file for all Zaber scripts with support for overlays and environments
* **Templates:** Parsing of both strings and files
* **Pathing:** Support for application directories
* **Logging:** Support for logging for individual library files and other packages
* **Emails:** Sending via SMTP using basic or templated emails including attachments
* **Initialization:** Provides a single entry point that can be hooked for unified subpackage initialization
* **Namespace sharing:** Allows the sharing of izaber.* namespace with other packages

This library came about after a number of different scripts were written around the office with each using a different configuration file doing similar tasks. 
For instance, the library that talked to ZERP has been through 2 version with as many configuration file formats.
The hope is that this library will provide enough of a foundation, yet be flexible enough to handle future needs within IT at Zaber.

Basic Concepts
--------------

This library is opininated. It dictates where certain things should be and how some parts of your code should be written. Sorry about that.

A configuration file named "``zaber.yaml``" is expected in the home directory "``~``" which varies depending on OS:

* **Linux:** ``/home/yourusername/zaber.yaml``
* **MacOS:** ``/Users/yourusername/zaber.yaml``
* **Windows:** ``\Users\yourusername\zaber.yaml``

The contents typically looks something similar to this::

  default:
    log:
        level: 10
    email:
        host: mail.example.com
        from: automatedsender@example.com
        to: recipient@example.com
    paths:
        path: ~

This configuration file will allow any iZaber based script to discover all the requisite options for things such as template and data files, connection parameters, and other options at a user-specific level. It also has the benefit of allowing sensitive data to be easily stored outside of the source directory preventing accidental commits of things such as passwords.

The bare minmum script might look something like this::

  #!/usr/bin/python

  from izaber import initialize, config

  # Initialize the library, load the config, inform the system that the application key is 'example'
  initialize('example') 

  # reach in and grab a configuration value
  print "The email host is {}".format(config.email.host) 

The initialize function is actually quite complex and allows for on-demand initialization of services and dependancies. 
Once the function is complete, the system should be prepared for usage in your application.

The simple example here, it only seeks loads the ``~/zaber.yaml`` into the ``config`` object.

In the following section, more complex scripts are demonstrating some using the various services available.

Paths
-----

Many scripts require various directories and files be it for data input or output. The paths service makes them easier to create and access.

If a configuration like the following is given::

  default:
    paths:
        path: '~'
        template_path: '{{path}}/templates'
        reports_path: '{{data_path}}/reports'
        data_path: '{{path}}/data'
        daily_report_path: '{{reports_path}}/{{date}}'

There are 4 paths here ``path``, ``template_path``, ``data_path``, and ``reports_path``. 

The one path that's really important is ``path``. This izaber services will assume that this directory is the script's home directory, things like log files will be automatically dumped into it.

There's templating support via jinja2 that handles the ``{{keyword}}`` syntax. You can do more complex stuff with it too if you *really* want.

When looking at ``reports_path``, the fully parsed path will become ``~/data/reports``. 

The entries do not need to be in any particular order, just that they don't end up referencing each other in a way that can't be resolved.

In code, accessing the directories is pretty straightforward::

  #!/usr/bin/python

  from izaber import initialize, config
  from izaber.paths import paths

  # Initialize the library, load the config, inform the system that the application key is 'example'
  initialize('example') 

  # Show the reports_path
  print paths.reports_path

  # Create a new file report
  # This opens a write filehandle to ~/data/reports/report_YYYY-MM-DD.csv 
  rep_fh = paths.reports_path.open('report_{{date}}.csv','w')
  rep_fh.write('Hello There!')
  rep_fh.close()

The initialization will load the directories and prepare them for use. Be aware that paths are automatically created when the initialization takes place. That is, the system will calculate the list of paths then perform an os.makedirs on each one.

The path also become an accessible property in the paths object. With a path object, you can perform actions such as file opens relative to that directory path.

Templates
---------

The templating system uses jinja2.

While there's no problems using jinja2 library directly, there's some additional supporting functions provided via iZaber that might be of interest.

There are two functions of interest one for strings and the other for files.

=========================   =======  ================================================
Function                    Returns  Description
=========================   =======  ================================================
parse(template,**tags)      string   takes a file path (that will be parsed by paths)
parsestr(template,**tags)   string   takes a string that's parsed as a template
=========================   =======  ================================================

Usage is pretty straight-forward, import the functions then make use of them.

For this example, this will use the same configuration as the previous example::

  default:
    paths:
        path: '~'
        template_path: '{{path}}/templates'
        reports_path: '{{data_path}}/reports'
        data_path: '{{path}}/data'
        daily_report_path: '{{reports_path}}/{{date}}'

Then, the code can look something like this::

  #!/usr/bin/python

  from izaber import initialize, config
  from izaber.paths import paths
  from izaber.templates import parse, parsestr

  # Initialize the library, load the config, inform the system that the application key is 'example'
  initialize('example2') 

  # Load, parse and print the template located at ~/templates/example.html
  print parse('{{path}}/templates/example.html',key1='value1',key2='value2')

  # parse and print the provided string template
  template_str = "Hello {{name}}! It's currently {{time}}"
  print parsestr(template_str,name='Example Name')

Script Configuration Overrides
------------------------------

Scripts will often need slightly different parameters. Not all scripts will want to share the same application home path, that'd just get frustrating. Configuration overlays to the rescue.

In this example, let's say we have a new script called 'example2' that runs periodic reports and it's important that it has its own location for reports.

It's possible to override specific default parameters for only 'example2' while retaining all the other properties.

Amending the configuration file to look like this::

  default:
    paths:
        path: '~'
        template_path: '{{path}}/templates'
        reports_path: '{{data_path}}/reports'
        data_path: '{{path}}/data'
        daily_report_path: '{{reports_path}}/{{date}}'
    example2:
        paths:
            reports_path: '{{path}}/example2reports'


With this configuration file, the new section, ``default.example2``, will be overlayed on top of the default configuration properties if requested.

How to request to have the overlay performed? A small change to the initialization is required::

  #!/usr/bin/python

  from izaber import initialize, config
  from izaber.paths import paths

  # Initialize the library, load the config, inform the system that the application key is 'example2'
  initialize('example2') 

  # Show the reports_path
  print paths.reports_path

  # Create a new file report
  # This opens a write filehandle to ~/data/example2reports/report_YYYY-MM-DD.csv 
  rep_fh = paths.reports_path.open('report_{{date}}.csv','w')
  rep_fh.write('Hello There')
  rep_fh.close()

The only change from the previous example is modifying the ``initialize('example2')``.

This overlaying feature allows for resources, such as email server configuration, to be shared across the scripts but provide flexiblity where needed.

Production, Sandboxes and Development
-------------------------------------

It's probably best not to always be testing scripts against the production servers.

The configuration system also provides a means to switch between sets of configurations or *environments* to overlay parameters to nerf the damage capacity of a script.

The previous examples all used ``default`` environment. This happens to be a particularly special environment as it's the root environment.

Other environments, similar to application overlays, as they are created, they will still rely upon the ``default`` environment for missing values.

Let's say that for the previous example, it would be nice to have a test directory for the data and reports.

To configure, amend the configuration to look like this::


  default:
    paths:
        path: '~'
        template_path: '{{path}}/templates'
        reports_path: '{{data_path}}/reports'
        data_path: '{{path}}/data'
        daily_report_path: '{{reports_path}}/{{date}}'
    example2:
        paths:
            reports_path: '{{path}}/example2reports'
  test:
      paths:
          path: '~/test'

In code, to tell the initialize script to reference the test environment, the previous example can be amended to:: 

  #!/usr/bin/python

  from izaber import initialize, config
  from izaber.paths import paths

  # Initialize the library, load the config, inform the system that the application key is 'example2'
  initialize('example2',environment='test') 

  # Show the reports_path
  print paths.reports_path

  # Create a new file report
  # This opens a write filehandle to ~/test/data/example2reports/report_YYYY-MM-DD.csv 
  rep_fh = paths.reports_path.open('report_{{date}}.csv','w')
  rep_fh.write('Hello There')
  rep_fh.close()

The only difference was to update the call to ``initialize(...)`` to include ``environment='test'``. 

This tells the system to first search ``test`` environment for requisite data before looking at the ``default`` environment.

Normally tweaking the environment value is not done via code but by providing a method of changing the environment via command-line.

Logging
-------

This library hooks into Python's ``logging`` service and comes along when using the paths service.

If we wanted to see all logging for all levels (normally the library is set to only report warnings and more urgent messages) we can amend the configuration file so::

  default:
    log:
        level: 10
    paths:
        path: '~'
        template_path: '{{path}}/templates'
        reports_path: '{{data_path}}/reports'
        data_path: '{{path}}/data'
        daily_report_path: '{{reports_path}}/{{date}}'


The numeric level values correspond so:

========  =======
Level     Numeric
========  =======
CRITICAL  50
ERROR     40
WARNING   30
INFO      20
DEBUG     10
========  =======

In this case, we're setting the debug level to ``10`` or returns anything ``DEBUG`` and up.

It's also possible to directly set other parameters here:

============= =============================
Option        Description
============= =============================
level         filter out everything above this level
filename      paths compatible filepath
filemode      usually 'a'
fileencoding  usually 'utf8'
format        log format in logging.Formatter compatible format
dateformat    how to display dates
============= =============================

Using it then, is pretty straightforward. Here's an example that just logs when a script starts and finishes::

  #!/usr/bin/python

  import time

  from izaber import initialize, config, log
  from izaber.paths import paths

  # Initialize the library, load the config, inform the system that the application key is 'example'
  initialize('example') 

  # Log when we start
  log.info('Script started!')

  # Layabout for a few seconds
  time.sleep(3)

  # And log completion
  log.debug('Script ended!')

Upon execution, the ``log.info('...')`` will cause the logger to append an informational message to a log file located at ``{{path}}/izaber.log``, which in this case would be ``~/izaber.log``.

Just before completion, the ``log.debug('...')`` will request the logger to append a debug message to the log file.

If the log level was set to something higher, for instance ``20``, the ``log.debug`` message would not have been sent to the log file.


Sending Emails
--------------

Beyond opening files, it's also nice to be able to communicate. This example will bring in email and logging support.

The configuration file will need information to the email server, which can be amended from the previous example like this:: 

  default:
    log:
        level: 10
    paths:
        path: '~'
        template_path: '{{path}}/templates'
        reports_path: '{{data_path}}/reports'
        data_path: '{{path}}/data'
        daily_report_path: '{{reports_path}}/{{date}}'
    email:
        host: 'mail.example.com'
        from: 'automatedsender@example.com'
        to: 'recipient@example.com'


For the script it will look like the following::

  #!/usr/bin/python

  from izaber import initialize, config
  from izaber.email import mailer

  # Initialize the library, load the config, inform the system that the application key is 'example'
  initialize('example') 

  # Load the templated email and send it
  mailer.template_send('{{path}}/myemail.email')

The line ``from izaber.email import mailer`` will add the email subsystem to the library and initialize it upon encountering the ``initialize('example')``.

The new line ``mailer.template_send('{{path}}/myemail.email')`` tells the imported mailer object to pull the template file located at ``{{path}}/myemail.email``, parse it and send it off to the recipient. The ``{{path}}`` is simply a shorthand to substitute the current application's path into it. In this case it would become ``~/myemail.email``.

Upon sending the email to the recipient, the system will also log the *from*, *to*, *subject* and *datetime* to the global log file. 
By default the log is located at ``{{path}}/izaber.log``.

The email template can look like a standard email except that it will be parsed via jinja2 first.

It should follow the same format that email.parser should like, something like this::

  From: {{config.email.from}}
  To: {{config.email.to}}
  Subject: Hi from automated script on {{date_iso}}

  <h1>TEST!</h1>

  <p>This is just a test email sent from an iZaber script.</p>

Since we like the ability to format our text, the body portion of the email will be treated as HTML. The library will also create a text-only alternative to allow more primitive clients readability.


Sending Attachments
-------------------

The previous example only allowed for a message to be sent. What about attachments?

To do that, the configuration file can remain the same as the above example in ``~/zaber.yaml``::

  default:
    email:
        host: mail.example.com
        from: automatedsender@example.com
        to: recipient@example.com
    paths:
        path: ~

The email too, can be left as-is in ``~/myemail.email``::

  From: {{config.email.from}}
  To: {{config.email.to}}
  Subject: Hi from automated script on {{date_iso}}

  <h1>TEST!</h1>

  <p>This is just a test email sent from an iZaber script.</p>

The code, however, must be amended::

  #!/usr/bin/python

  from izaber import initialize, config
  from izaber.email import mailer

  # Initialize the library, load the config, inform the system that the application key is 'example'
  initialize('example') 

  # Get a message object
  msg = mailer.template_parse('{{path}}/myemail.email')

  # Get an attachment object
  attachment = mailer.attachment_create('{{path}}/myattachment.zip')

  # Attach a file
  msg.attach(attachment)

  # And send the email off
  mailer.message_send(msg)

Adding multiple attachments is simple, loop on creating a new attachment object then attaching to the outgoing message.

Debugging Emails
----------------

As scripting with emails can make a small embarassing situation and turn it into a massive one, there's also facility for debugging.

If you wish to isolate debugging behaviour to just the email module, update the configuration so ``config.email.debug`` is ``true``. 

If you want the debug mode enabled globally, you can set ``config.debug`` to ``true``.

For example the previous examples' configuration file could be modified to look so::

  default:
    debug: true
    log:
        level: 10
    email:
        debug: true
        host: mail.example.com
        from: automatedsender@example.com
        to: recipient@example.com
    paths:
        path: ~

Instead of sending the email, the raw email will be logged to your system log. There are two ``debug: true`` entries in there that if all you want to do is debug email, it's redundant.