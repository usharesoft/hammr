.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _builder-iso:

ISO
===

Default builder type: ``ISO``

Require Cloud Account: No

This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The ISO builder provides information for building ISO images.

The ISO builder section has the following definition:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "ISO",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for ISO: ``ISO``. To get the available builder type, please refer to :ref:`command-line-format`
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* diskSize (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.

Example
-------

The following example shows an ISO builder.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "ISO"
	    }
	  ]
	}
