.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _builder-raw:

Raw
===

Builder type: ``raw``
Require Cloud Account: No

The Raw builder provides information for building a Raw Virtual Disk compatible machine images.
The Raw builder section has the following definition:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "raw",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.
* ``type`` (mandatory): the builder type: ``raw``

Example
-------

The following example shows a Raw builder.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "raw",
	      "hardwareSettings": {
	        "memory": 1024
	      }
	    }
	  ]
	}
