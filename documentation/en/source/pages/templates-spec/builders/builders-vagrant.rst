.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-vagrant:

Vagrant Base Box
================

Default builder type: ``Vagrant Base Box``

Require Cloud Account: No

The Vagrant builder provides information for building Vagrant base-box machine images.
This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The Vagrant builder section has the following definition when using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Vagrant Base Box
		# the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "Vagrant Base Box",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Vagrant: ``Vagrant Base Box``. To get the available builder type, please refer to :ref:`command-line-format`
* ``hardwareSettings`` (mandatory): an object providing hardware settings to be used for the machine image. The following valid keys for hardware settings are:
	* ``memory`` (mandatory): an integer providing the amount of RAM to provide to an instance provisioned from the machine image (in MB).
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.
* ``osUser`` (optional): a string providing the user used to authenticate to the vagrant base box. This is mandatory if the base box is private, otherwise this value is ignored and the user ``vagrant`` is used.
* ``publicBaseBox`` (optional): a boolean determining if the base box to be created is a public base box or not. When public, the os user is vagrant and uses the public (insecure) public key as described in the vagrant documentation
* ``sshKey`` (optional): an object providing the public SSH key information to add to the base box. The object contains:
	* ``name`` (mandatory): a string providing the name of the public ssh key
	* ``publicKey`` (mandatory): a string providing the public ssh key. A public key must begin with string ``ssh-rsa`` or ``ssh-dss``.  This is mandatory if the base box is private, otherwise this value is ignored and the `default public ssh key <https://github.com/mitchellh/vagrant/blob/master/keys/vagrant.pub>`_ is used.

.. note:: You can get copies of the SSH keypairs for public base boxes `here <https://github.com/mitchellh/vagrant/tree/master/keys>`_.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Examples
--------

Basic Example: Public Base Box
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows a Vagrant builder creating a public base box.

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Vagrant Base Box
	  hardwareSettings:
	    memory: 1024
	  publicBaseBox: true

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Vagrant Base Box",
	      "hardwareSettings": {
	        "memory": 1024
	      },
	      "publicBaseBox": true
	    }
	  ]
	}

Private Base Box Example
~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows a Vagrant builder for a private base box (note, that the values used is the same for building a public base box)

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Vagrant Base Box
	  hardwareSettings:
	    memory: 1024
	  publicBaseBox: false
	  osUser: vagrant
	  sshKey:
	    name: myVagrantPublicKey
	    publicKey: ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ==
	      vagrant insecure public key

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Vagrant Base Box",
	      "hardwareSettings": {
	        "memory": 1024
	      },
	      "publicBaseBox": false,
	      "osUser": "vagrant",
	      "sshKey": {
	        "name": "myVagrantPublicKey",
	        "publicKey": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key"
	      }
	    }
	  ]
	}
