.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-bundle-license:

license
=======

Within a ``bundle``, the ``license`` sub-section describes the license information or EULA for the files that make up the bundle.

The definition of a ``license`` section when using YAML is:

.. code-block:: yaml

	---
	license:
	  # the license declaration goes here.

If you are using JSON:

.. code-block:: javascript

	"license": {
	    ...the license declaration goes here.
	}

The valid keys to use within a license are:

* ``name`` (mandatory): a string providing the name of the license.
* ``source`` (mandatory): a string providing the location of where to get the license. This can be a filesystem path or URL.

Example
-------

The following example shows how to declare a license for a bundle.

If you are using YAML:

.. code-block:: yaml

	---
	license:
	  name: license.html
	  source: "/home/joris/demo/apache-license.html"

If you are using JSON:

.. code-block:: json

	{
	  "license": {
	    "name": "license.html",
	    "source": "/home/joris/demo/apache-license.html"
	  }
	}