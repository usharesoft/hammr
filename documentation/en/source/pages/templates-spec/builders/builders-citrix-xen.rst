.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _builder-citrix-xen:

citrix-xen
==========

Require Cloud Account: No

The Citrix XenServer builder provides information for building XenServer compatible machine images.

The Citrix XenServer builder section has the following definition:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "citrix-xen",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``hardwareSettings`` (mandatory): an object providing hardware settings to be used for the machine image. The following valid keys for hardware settings are:
	* ``memory`` (mandatory): an integer providing the amount of RAM to provide to an instance provisioned from the machine image (in MB).
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.
* ``type`` (mandatory): the builder type, ``xenserver``

Example
-------

The following example shows a Citrix XenServer builder.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "citrix-xen",
	      "hardwareSettings": {
	        "memory": 1024
	      }
	    }
	  ]
	}
