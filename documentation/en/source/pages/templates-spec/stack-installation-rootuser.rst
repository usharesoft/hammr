.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-installation-rootuser:

rootUser
========

Within an :ref:`stack-installation`, the ``rootUser`` sub-section describes information for the root user to be created as part of the machine image build. If no root user information is provided, when an instance is provisioned from the machine image, the root user password is prompted.

The definition of a ``rootUser`` section when using YAML is:

.. code-block:: yaml

	---
	rootUser:
	  # the root user definition goes here.

If you are using JSON:

.. code-block:: javascript

	"rootUser": {
	    ...the root user definition goes here.
	}

The valid keys to use within a rootUser are:

* disablePasswordLogin (optional): a boolean to determine whether to disable the ability for the root user to login into a running instance using the root password.
* password (optional): a string providing the root user password. A blank password "" is valid.
* setPassword (mandatory): a boolean to determine whether to preset a password during the build or prompt the user to add a password during first boot of the instance.
* sshKeys (optional): an array of objects providing one or more public ssh keys for the root user. For more information, refer to the :ref:`stack-installation-sshkeys` sub-section.

Sub-sections
------------

The root user sub-sections are:

.. toctree::
   :titlesonly:

   stack-installation-sshkeys
  

Examples
--------

Basic Example
~~~~~~~~~~~~~

The following example describes the basic root user information.

If you are using YAML:

.. code-block:: yaml

	---
	rootUser:
	  password: welcome-not-a-good-password

If you are using JSON:

.. code-block:: json

	{
	  "rootUser": {
	    "password": "welcome-not-a-good-password"
	  }
	}

Disabling Password Login
~~~~~~~~~~~~~~~~~~~~~~~~

You can easily disable root password login as a security measure by doing the following:

If you are using YAML:

.. code-block:: yaml

	---
	rootUser:
	  password: welcome-not-a-good-password
	  disablePasswordLogin: true

If you are using JSON:

.. code-block:: json

	{
	  "rootUser": {
	    "password": "welcome-not-a-good-password",
	    "disablePasswordLogin": true
	  }
	}
