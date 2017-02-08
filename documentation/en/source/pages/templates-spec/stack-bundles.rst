.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _stack-bundles:

bundles
=======

Within a ``stack``, the ``bundles`` sub-section describes any custom software to be added to the filesystem of the machine image during the build phase. Software bundles can contain any file, archive or native package. Native packages can be installed and archives can be uncompressed as part of this process.

The definition of a ``bundles`` section when using YAML is:

.. code-block:: yaml

	---
	bundles:
	- # the list of bundles goes here.

If you are using JSON:

.. code-block:: javascript

	"bundles": [
	    ...the list of bundles goes here.
	]

The valid keys to use within a bundle are:

* ``description`` (optional): a string describing what the bundle does or contains.
* ``destination`` (mandatory): a string providing the target directory where to add the files in the filesystem.
* ``files`` (mandatory): an array of objects describing the files, archives or packages contained in the bundle. See the :ref:`stack-bundle-files` sub-section for available keys.
* ``license`` (optional): an object providing the license information for the bundle. See the :ref:`stack-bundle-license` sub-section for available keys.
* ``name`` (mandatory): a string providing the name of the bundle.
* ``version`` (mandatory): a string providing the version of the bundle.

The destination string that describes where to add the files in the bundle is ignored for native packages that have the option to be installed during the build process.

Sub-sections
------------

Bundle sub-sections are:

.. toctree::
   :titlesonly:

   stack-bundle-files
   stack-bundle-license
   

Examples
--------

Basic Example
~~~~~~~~~~~~~

The following example describes the mandatory information in a bundle to be uploaded and used in the template. All the files described in the bundle are placed in the ``/tmp/wordpress`` directory.

If you are using YAML:

.. code-block:: yaml

	---
	bundles:
	- name: wordpress
	  version: '3.5'
	  destination: "/tmp/wordpress"
	  files:
	  - # add files definition here.
	- name: wordpress language pack
	  version: '3.5'
	  destination: "/tmp/wordpress"
	  files:
	  - # add files definition here.

If you are using JSON:

.. code-block:: json

	{
	  "bundles": [
	    {
	      "name": "wordpress",
	      "version": "3.5",
	      "destination": "/tmp/wordpress",
	      "files": [
	          ...add files definition here.
	      ]
	    },
	    {
	      "name": "wordpress language pack",
	      "version": "3.5",
	      "destination": "/tmp/wordpress",
	      "files": [
	          ...add files definition here.
	      ]
	    }
	  ]
	}

Adding a Description and License
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example show how you can add license information and a description to the bundle.

If you are using YAML:

.. code-block:: yaml

	---
	bundles:
	- name: wordpress
	  version: '3.5'
	  description: The wordpress files from wordpress.org
	  destination: "/tmp/wordpress"
	  files:
	  - # add files definition here (see files sub section)
	  license:
	    # add license definition here (see license sub section)

If you are using JSON:

.. code-block:: json

	{
	  "bundles": [
	    {
	      "name": "wordpress",
	      "version": "3.5",
	      "description": "The wordpress files from wordpress.org",
	      "destination": "/tmp/wordpress",
	      "files": [
	          ...add files definition here (see :ref:`stack-bundle-files` sub-section)
	      ],
	      "license": {
	          ...add license definition here (see :ref:`stack-bundle-license` sub-section)
	      }
	    }
	  ]
	}

