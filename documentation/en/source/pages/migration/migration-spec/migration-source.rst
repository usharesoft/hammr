.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _migration-source:

Source
======

The source section describes the live system to migrate.

The definition of a ``source`` section when using YAML is:

.. code-block:: yaml

	---
	source:
	  # the source definition goes here

If you are using JSON:

.. code-block:: javascript

	{
		"source": {
		    ...the source definition goes here.
		}
	}

The valid keys to use within a source are:

* ``host`` (mandatory): a string providing the URL of the live system.
* ``ssh-port`` (optional): an integer providing the ssh port of the running system (default: 22).
* ``user`` (mandatory): a string providing the user login to authenticate to the live system.
* ``password`` (optional): a string providing the user password to authenticate to the live system.
* ``exclude`` (optional): a list of non-native files or directories to exclude during the deep scan of the live system.