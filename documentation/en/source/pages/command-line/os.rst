.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _command-line-os:

os
==

Displays all the operating systems available to use when creating templates. The usage is:

.. code-block:: shell

	usage: hammr os [sub-command] [options]


Sub Commands
------------

``list`` sub-command
~~~~~~~~~~~~~~~~~~~~

Displays all the operating systems available to use by the user.

``search`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Operating System package search.

	* ``--id`` (mandatory): the ID of the OS
	* ``--pkg`` (mandatory): Regular expression of the package:
		* "string" : search all packages wich contains "string"
		* "^string": search all packages wich start with "string"
		* "string$": search all packages wich end with "string"
