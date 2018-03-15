.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-installation-sshkeys:

sshKeys
=======

The ``sshKeys`` sub-section describes one or more public SSH keys that can be used for a particular user.

The definition of an ``sshKeys`` section when using YAML is:

.. code-block:: yaml

	---
	sshKeys:
	- # the list of ssh keys goes here.

If you are using JSON:

.. code-block:: javascript

	"sshKeys": [
	    ...the list of ssh keys goes here.
	]

The valid keys to use within a sshKey are:

* ``name`` (mandatory): a string providing the name of the public SSH key
* ``publicKey`` (mandatory): a string providing the public key content. A public key must begin with string ``ssh-rsa`` or ``ssh-dss``

Example
-------

This example shows how to provide an ssh key for the root user of the operating system.

If you are using YAML:

.. code-block:: yaml

	---
	sshKeys:
	- name: admin-public
	  publicKey: ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ

If you are using JSON:

.. code-block:: json

	{
	  "sshKeys": [
	    {
	      "name": "admin-public",
	      "publicKey": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ"
	    }
	  ]
	}

