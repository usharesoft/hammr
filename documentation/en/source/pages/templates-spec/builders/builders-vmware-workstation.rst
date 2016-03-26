.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _builder-vmware-workstation:

VMware Workstation
==================

Builder type: ``vmware``
Require Cloud Account: No

The VMware Workstation builder provides information for building VMware Workstation compatible machine images.
The VMware Workstation builder section has the following definition:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "vmware",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

The VMware Workstation builder has the following valid keys:

* ``hardwareSettings`` (mandatory): an object providing hardware settings to be used for the machine image. The following valid keys for hardware settings are:
	* ``memory`` (mandatory): an integer providing the amount of RAM to provide to an instance provisioned from the machine image (in MB).
	* ``hwType`` (optional): an integer providing the hardware type for the machine image. This is the VMware hardware type: 4 (ESXi>3.x), 7 (ESXi>4.x) or 9 (ESXi>5.x)
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.
* ``type`` (mandatory): the builder type: ``vmware``

Example
-------

The following example shows an VMware Workstation builder.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "vmware",
	      "hardwareSettings": {
	        "memory": 1024,
	        "hwType": 7
	      }
	    }
	  ]
	}
