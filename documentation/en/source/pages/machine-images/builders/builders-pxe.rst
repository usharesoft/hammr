.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-pxe:

PXE
===

Default builder type: ``PXE``

Require Cloud Account: No

This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The PXE builder provides information for building PXE images. PXE images are used using PXE boot. It is possible to download them through a IPXE shell that calls RESTFUL resources provided by your forge.

The PXE builder section has the following definition when using YAML:

.. code-block:: yaml

	---
	builders:
	- type: PXE
		# the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "PXE",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for PXE: ``PXE``. To get the available builder type, please refer to :ref:`command-line-format`
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* diskSize (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Example
-------

The following example shows an PXE builder.

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: PXE

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "PXE"
	    }
	  ]
	}
