.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-installation-users:

users
=====

Within an :ref:`stack-installation` section, the ``users`` sub-section describes extra operating system users to create as part of the machine image build process.

The definition of a ``users`` section when using YAML is:

.. code-block:: yaml

	---
	users:
	- # the list of users goes here.

If you are using JSON:

.. code-block:: javascript

	"users": [
	    ...the list of users goes here.
	]

The valid keys to use within a user are:

* ``fullName`` (mandatory): a string providing the full name of the user. The same value as ``name`` can be used.
* ``homeDir`` (mandatory): a string providing the home directory of the user. Recommended default: ``/home/username`` where username is the same value as ``name``
* ``name`` (mandatory): a string providing the name of the user. The name cannot contain any spaces.
* ``password`` (optional): a string providing the user password.
* ``primaryGroup`` (optional): a string providing the user’s primary group. If no primary group is given, then the primary group is the same as name.
* ``shell`` (mandatory): a string providing the default shell environment for the user. Recommended default is ``/bin/bash``.
* ``secondaryGroups`` (optional): a string providing one or more group names separated by a comma (,).
* ``systemUser`` (optional): a boolean determining if the user is a system user.
* ``userId`` (optional): an integer providing the unique Id of the user. This number must be greater than 1000. If the user is a system user, then this number must be greater than 201.

Examples
--------

Basic Example
~~~~~~~~~~~~~~

The following example provides the minimal information to create users during a build. As no ``userId`` is specified, the next available user Id numbers are used automatically during the build of the machine image. Furthermore, as no primary group is provided, the primary group will have the same name as the user name.

If you are using YAML:

.. code-block:: yaml

	---
	users:
	- name: joris
	  fullName: joris
	  homeDir: "/home/joris"
	  shell: "/bin/bash"
	- name: yann
	  fullName: yann dorcet
	  homeDir: "/home/ydorcet"
	  shell: "/bin/bash"

If you are using JSON:

.. code-block:: json

	{
	  "users": [
	    {
	      "name": "joris",
	      "fullName": "joris",
	      "homeDir": "/home/joris",
	      "shell": "/bin/bash"
	    },
	    {
	      "name": "yann",
	      "fullName": "yann dorcet",
	      "homeDir": "/home/ydorcet",
	      "shell": "/bin/bash"
	    }
	  ]
	}

More Complex Example
~~~~~~~~~~~~~~~~~~~~

This example shows how you can provide group information, set a user Id and make a user a system user.

If you are using YAML:

.. code-block:: yaml

	---
	users:
	- name: joris
	  fullName: joris
	  userId: 2222
	  primaryGroup: joris
	  secondaryGroups: dev,france
	  homeDir: "/home/joris"
	  shell: "/bin/bash"
	- name: yann
	  fullName: yann dorcet
	  systemUser: true
	  userId: 400
	  primaryGroup: yann
	  secondaryGroups: admin,dev,france
	  homeDir: "/home/ydorcet"
	  shell: "/sbin/nologin"

If you are using JSON:

.. code-block:: json

	{
	  "users": [
	    {
	      "name": "joris",
	      "fullName": "joris",
	      "userId": 2222,
	      "primaryGroup": "joris",
	      "secondaryGroups": "dev,france",
	      "homeDir": "/home/joris",
	      "shell": "/bin/bash"
	    },
	    {
	      "name": "yann",
	      "fullName": "yann dorcet",
	      "systemUser": true,
	      "userId": 400,
	      "primaryGroup": "yann",
	      "secondaryGroups": "admin,dev,france",
	      "homeDir": "/home/ydorcet",
	      "shell": "/sbin/nologin"
	    }
	  ]
	}

.. warning:: By setting ``/sbin/nologin`` the user will not be able to log in via the machine's console.
