.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _template-stack:

Stack
=====

Within a template, the stack section describes the packages, files and configuration information required to be added when building a machine image. It can also contain low level installation information (for example keyboard settings, partitioning, timezone etc) to be configured as part of the build or prompted during the first boot of an instance using the machine image.

The definition of a ``stack`` section when using YAML is:

.. code-block:: yaml

	---
	stack:
	  # the stack definition goes here

If you are using JSON:

.. code-block:: javascript

	{
		"stack": {
		    ...the stack definition goes here.
		}
	}

The valid keys to use within a stack are:

* ``name`` (mandatory): a string providing the name of the stack
* ``version`` (mandatory): a string providing the version of the stack
* ``description`` (optional): a string providing a description of what the stack oes
* ``os`` (mandatory): an object providing the operating system to use when building the machine image. You must have access to this operating system in UForge. This object may include specific packages to install from the operating system repository. For more information, refer to the :ref:`stack-os` sub-section.
* ``bundles`` (optional): an array of objects describing any software bundles (can be native packages, tarballs, jars, wars etc) to upload and use when building the machine image. For more information, refer to the :ref:`stack-bundles` sub-section.
* ``installation`` (optional): an object providing low-level installation or first boot options. Some options can be pre-configured as part of the build or prompted by the end-user to provide when provisioning an instance from the machine image. For more information, refer to the :ref:`stack-installation` sub-section.
* ``config`` (optional): an array of objects describing any configuration scripts to execute when an instance is booted from the machine image.  For more information, refer to the :ref:`stack-config` sub-section.

Stack sub-sections are:

.. toctree::
   :titlesonly:

   stack-os
   stack-bundles
   stack-installation
   stack-config

.. rubric:: Example

The following example shows a simple ``stack`` definition, when using YAML:

.. code-block:: yaml

	---
	stack:
	  name: CentOS Base Template
	  version: '6.4'
	  description: This is a CentOS core template.
	  os:
		name: CentOS
		version: '6.4'
		arch: x86_64
		profile: Minimal

If you are using JSON:

.. code-block:: json

	{
	  "stack": {
	    "name": "CentOS Base Template",
	    "version": "6.4",
	    "description": "This is a CentOS core template.",
	    "os": {
	      "name": "CentOS",
	      "version": "6.4",
	      "arch": "x86_64",
	      "profile": "Minimal"
	    }
	  }
	}

