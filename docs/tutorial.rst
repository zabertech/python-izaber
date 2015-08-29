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
        path: ~
        template_path: {{path}}/templates
        reports_path: {{data_path}}/reports
        data_path: {{path}}/data

There are 4 paths here ``path``, ``template_path``, ``data_path``, and ``reports_path``. 

When looking at ``reports_path``, the fully parsed path will become ``~/data/reports``. 

The entries do not need to be in any particular order, just that they don't end up referencing each other in a way that can't be resolved.

In code, accessing the directories is pretty straightforward::

  #!/usr/bin/python

  from izaber import initialize, config
  from izaber.paths import paths

  # Initialize the library, load the config, inform the system that the application key is 'example'
  initialize('example') 

  # Show the reports_path
  print paths.report_path

  # Create a new file report
  # This opens a write filehandle to ~/data/reports/report_YYYY-MM-DD.csv 
  rep_fh = paths.report_path.open('report_{date}.csv','w')
  rep_fh.write('Hello,There)
  rep_fh.close()

Sending Emails
--------------

Beyond opening files, it's also nice to be able to communicate. This example will bring in email and logging support.

The configuration file will need information to the email server, which can be amended from the previous example like this:: 

  default:
    email:
        host: mail.example.com
        from: automatedsender@example.com
        to: recipient@example.com
    paths:
        path: ~
        template_path: {{path}}/templates
        reports_path: {{data_path}}/reports
        data_path: {{path}}/data


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



