.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _launch-hammr:

Launching hammr
===============

Hammr is a command-line tool, allowing you to specify commands that get executed by hammr. Each command may have one or more sub-commands and optional parameters. Hammr provides inbuilt help. To list all the main options, use the ``-h``, ``--help`` flags or ``TAB``.

.. code-block:: shell

	$ hammr -h
	usage: hammr [-h] [-a URL] [-u USER] [-p PASSWORD] [-v] [cmds [cmds ...]]
	To get more information on a sub-command, use the -h, --help flags or TAB for more information

	$ hammr template -h
	======================================================================================================
	Template help
	======================================================================================================
	build                         | Builds a machine image from the template
	clone                         | Clones the template. The clone is copying the meta-data of the template 
	create                        | Create a new template and save to the UForge server
	delete                        | Deletes an existing template
	export                        | Exports a template by creating an archive (compressed tar file)
	help                          | List available commands with "help" or detailed help with "help cmd".
	import                        | Creates a template from an archive
	list                          | Displays all the created templates
	validate                      | Validates the syntax of a template configuration file      


Modes
-----

There are three different modes when launching hammr:

	* Classic command-line: used in shell scripts or via a terminal
	* Interactive mode: where hammr is launched once, providing you a prompt to execute hammr commands
	* Batch mode: allowing hammr to execute a series of commands from a file

When using the classic mode, the command ``hammr`` is used, followed by a command, sub-command and any options.  For example:

.. code-block:: shell

	$ hammr os list --url https://your-uforge.com/api -u username -p password

To enter interactive mode, launch the ``hammr`` command on its own. This provides a prompt, allowing you to enter commands and sub-commands the same way as you would in classic mode.

To use batch mode, create a file containing the list of commands you wish to launch in sequence and then provide this file to hammr via the batch command. For example if you wanted to list all the operating system available to you in batch mode, firstly create a file with the commands to launch, in this case ``os list``:

.. code-block:: shell

	$ vi batchfile
	os list

Launch hammr providing the batch file:

.. code-block:: shell

	$ hammr batch --file batchfile --url https://your-uforge.com/api -u username -p password
	os list 
	Getting distributions for [root] ...
	+-----+--------+---------+--------------+---------------------+-----------------+
	| Id  |  Name  | Version | Architecture |    Release Date     |    Profiles     |
	+=====+========+=========+==============+=====================+=================+
	| 121 | CentOS | 6.4     | x86_64       | 2013-03-01 14:01:26 | Server No X     |
	|     |        |         |              |                     | Server          |
	|     |        |         |              |                     | Minimal         |
	+-----+--------+---------+--------------+---------------------+-----------------+
	| 87  | Ubuntu | 12.04   | x86_64       | 2012-02-24 19:04:45 | Minimal Desktop |
	|     |        |         |              |                     | Server          |
	|     |        |         |              |                     | Minimal         |
	+-----+--------+---------+--------------+---------------------+-----------------+

Authentication
--------------

Communication between hammr and the UForge server is done via HTTPS. To send requests to the UForge server, hammr requires the following information:

	* UForge Server URL endpoint
	* Your account user name
	* Your password

This information can be passed to hammr either from command-line options or from a file.


Command-line Parameters
-----------------------

Authentication information can be passed to hammr via command-line options.  These options are:

	* ``-a`` or ``--url``: the UForge Server URL endpoint.  If the URL uses HTTPS, then the connection will be done securely (recommended), otherwise connection will be done via HTTP
	* ``-u`` or ``--user``: the user name to use for authentication
	* ``-p`` or ``--password``: the password to use for authentication

For example

.. code-block:: shell

	$ hammr os list --url https://your-uforge.com/api -u username -p password

These parameters need to be passed each time you wish to use the command-line.

.. _credential-file:

Using a Credential File
-----------------------

Rather than passing the authentication information as part of the command-line, you can instead store this information in a credential file (``credentials.json`` or ``credentials.yml``) that will be used every time hammr is launched.  Hammr searches for this file in a sub-directory named ``.hammr`` located in the home directory of the user launching hammr.

.. note:: If your AppCenter has a self-signed certificate, in order to use hammr with your AppCenter you must use a credentials file.

To use a credential file, go to the ``.hammr`` sub-directory and create the file ``credentials.yml``.

.. note:: You can also use JSON. In which case you need to create a file ``credentials.json``.

.. code-block:: shell

	$ cd ~/.hammr
	$ vi credentials.yml

Add the authentication and UForge URL endpoint to this file, using the following format:

.. code-block:: yaml

	---
	user: root
	password: password
	url: http://10.1.2.24/api
	acceptAutoSigned: false

If you are using JSON:

.. code-block:: json

	{
	  "user" : "root",
	  "password" : "password",
	  "url" : "http://10.1.2.24/api",
	  "acceptAutoSigned": false
	}


As this file contains security information, it is recommended to change the permissions on this file, so only you can read or write to it:

.. code-block:: shell

	$ chmod 600 credentials.yml

Now every time hammr is launched, you no longer need to provide the authentication information as part of the command-line. Hammr will automatically use the information contained in this file.

.. note:: The key ``acceptAutoSigned`` is to accept or not self-signed SSL certificates. Default value is ``false``.

.. _supervisor-mode:

Using Supervisor Mode
---------------------

UForge allows you to access UForge as another user if you have supervisor access. Supervisor access rights are assigned by the UForge administrator. 

.. warning:: Users with Supervisor Access will be able to log in as ANY of the users in the organization without entering a password. This right should be limited to support or managed services. Users with Supervisor Role needs to respect the privacy of the user data, according to current legislation.

To use hammr in supervisor mode you will need to enter your user name (UserA) as well as the user name of the account you want to access (UserB). For example:

.. code-block:: shell

	$ hammr os list --url https://uforge.usharesoft.com/api -u "UserA\UserB" -p password
