.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-vmware-workstation:

VMware Workstation
==================

Default builder type: ``VMware Server``

Require Cloud Account: No

The VMware Workstation builder provides information for building VMware Workstation compatible machine images.
This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The VMware Workstation builder section has the following definition when using YAML:

.. code-block:: yaml

	---
	builders:
	- type: VMware Server
		# the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "VMware Server",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

The VMware Workstation builder has the following valid keys:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for VMware Workstation: ``VMware Server``. To get the available builder type, please refer to :ref:`command-line-format`
* ``hardwareSettings`` (mandatory): an object providing hardware settings to be used for the machine image. The following valid keys for hardware settings are:
	* ``memory`` (mandatory): an integer providing the amount of RAM to provide to an instance provisioned from the machine image (in MB).
	* ``hwType`` (optional): an integer providing the hardware type for the machine image. This is the VMware hardware type: 4 (ESXi>3.x), 7 (ESXi>4.x) or 9 (ESXi>5.x)
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Example
-------

The following example shows a VMware Workstation builder.

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: VMware Server
	  hardwareSettings:
	    memory: 1024
	    hwType: 7

If you are using JSON:

.. code-block:: json

	{
		"builders": [
		{
	      "type": "VMware Server",
	      "hardwareSettings": {
	        "memory": 1024,
	        "hwType": 7
	      }
		}
	]
	}
