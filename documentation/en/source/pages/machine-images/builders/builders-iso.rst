.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-iso:

ISO
===

Default builder type: ``ISO``

Require Cloud Account: No

This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The ISO builder provides information for building ISO images.

The ISO builder section has the following definition when using YAML:

.. code-block:: yaml

	---
	builders:
	- type: ISO
		# the rest of the definition goes here.

If you are using JSON:

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

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Example
-------

The following example shows an ISO builder.

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: ISO

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "ISO"
	    }
	  ]
	}
