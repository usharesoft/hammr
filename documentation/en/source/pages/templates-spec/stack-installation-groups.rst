.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-installation-groups:

groups
======

Within an :ref:`stack-installation` section, the ``groups`` sub-section describes extra operating system groups to create as part of the machine image build process.

The definition of a ``groups`` section when using YAML is:

.. code-block:: yaml

	---
	groups:
	- # the list of groups goes here.

If you are using JSON:

.. code-block:: javascript

	"groups": [
	    ...the list of groups goes here.
	]

The valid keys to use within a group are:

* ``name`` (mandatory): a string providing the name of the group. The name cannot contain any spaces.
* ``systemGroup`` (optional): a boolean determining if the group is a system user.
* ``groupId`` (optional): an integer providing the unique Id of the group. This number must be greater than 1000. If the group is a system group, then this number must be greater than 201.

Examples
--------

Basic Example
~~~~~~~~~~~~~

The following example describes groups to be created during the build. As no ``groupId`` is specified, the next available group Id numbers are used automatically during the build of the machine image.

If you are using YAML:

.. code-block:: yaml

	---
	groups:
	- name: nginx
	- name: mongoDb

If you are using JSON:

.. code-block:: json

	{
	  "groups": [
	    {
	      "name": "nginx"
	    },
	    {
	      "name": "mongoDb"
	    }
	  ]
	}

System Groups and Group Ids
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example shows how you can pre-determine the ``groupId`` of the group to be created as well as making the group a system group.

.. warning:: A normal group’s Id must be greater than 1000. If the group is a system group, then this Id can start at 201.

If you are using YAML:

.. code-block:: yaml

	---
	groups:
	- name: nginx
	  groupId: 1033
	- name: mongoDb
	  systemGroup: true
	  groupId: 245

If you are using JSON:

.. code-block:: json

	{
	  "groups": [
	    {
	      "name": "nginx",
	      "groupId": 1033
	    },
	    {
	      "name": "mongoDb",
	      "systemGroup": true,
	      "groupId": 245
	    }
	  ]
	}