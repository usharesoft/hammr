.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _migration-destination:

Target
======

The target section describes the targeted cloud provider.

The definition of a ``target`` section when using YAML is:

.. code-block:: yaml

	---
	target:
	  # the target definition goes here

If you are using JSON:

.. code-block:: javascript

	{
		"target": {
		    ...the target definition goes here.
		}
	}

The valid keys to use within a target are:

* ``builder`` (mandatory): an object describing the format of the machine images to build.

Sub-Sections
------------

The ``target`` sub-sections are:

.. toctree::
   :titlesonly:

   ../../machine-images/builders/overview
