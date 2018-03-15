.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-hyper-v:

Hyper-V
=======

Default builder type: ``Hyper-V``

Require Cloud Account: No

This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The Hyper-V builder provides information for building Hyper-V compatible machine images.
The Hyper-V builder section has the following definition when using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Hyper-V
		# the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "Hyper-V",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Hyper-V: ``Hyper-V``. To get the available builder type, please refer to :ref:`command-line-format`
* ``hardwareSettings`` (mandatory): an object providing hardware settings to be used for the machine image. The following valid keys for hardware settings are:
	* ``memory`` (mandatory): an integer providing the amount of RAM to provide to an instance provisioned from the machine image (in MB).
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Example
-------

The following example shows a Hyper-V builder.

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Hyper-V
	  hardwareSettings:
	    memory: 1024

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Hyper-V",
	      "hardwareSettings": {
	        "memory": 1024
	      }
	    }
	  ]
	}
