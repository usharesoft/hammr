.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _command-line:

Command-Line
============

Hammr is launched by using the main command-line tool hammr. The hammr tool can be launched with other ``commands``, ``sub-commands`` and ``options``. The usage for the tool, can be shown by running hammr with the help options ``-h`` or ``--help``:

.. code-block:: shell

	$ hammr --help
	usage: hammr [-h] [-a URL] [-u USER] [-p PASSWORD] [-v] [cmds [cmds ...]]

The global ``options`` are:

* ``-h``, ``--help``: displays the usage
* ``-a URL``, ``--url URL``: the UForge server URL endpoint to use
* ``-u USER``, ``--user USER``: the user name used to authenticate to the UForge server
* ``-p PASSWORD``, ``--password PASSWORD``: the password used to authenticate to the UForge server
* ``-v``: displays the current version of the hammr tool

Hammr communicates with a UForge server instance, requiring authentication information as part of this authentication. The authentication information may be passed to hammr via the global options, however, there are other ways to pass this information. For more information, please refer to :ref:`authentication-methods` section of the documentation.

Below provides a list of the available ``commands``:

.. toctree::
   :titlesonly:

   account
   bundle
   deploy
   format
   platform
   image
   os
   quota
   scan
   template
