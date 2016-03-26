.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _builder-qcow2:

QCOW2
=====

Builder type: ``qcow2``
Require Cloud Account: No

The QCOW2 builder provides information for building a QCOW2 compatible machine images.
The QCOW2 builder section has the following definition:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "qcow2",
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
* ``type`` (mandatory): the builder type: ``qcow2``

Example
-------


The following example shows a QCOW2 builder.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "qcow2",
	      "hardwareSettings": {
	        "memory": 1024
	      }
	    }
	  ]
	}
