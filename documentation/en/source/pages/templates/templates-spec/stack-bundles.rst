.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

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

	"bundles": {
	    ...the list of bundles goes here.
	}

The valid keys to use within a bundle are:

* ``description`` (optional): a string describing what the bundle does or contains.
* ``destination`` (optional): a string providing the target directory where to add the files in the filesystem.
* ``files`` (mandatory): an array of objects describing the files, archives or packages contained in the bundle (each element can have another files key). See the :ref:`stack-bundle-files` sub-section for available keys.
* ``license`` (optional): an object providing the license information for the bundle. See the :ref:`stack-bundle-license` sub-section for available keys.
* ``name`` (mandatory): a string providing the name of the bundle.
* ``version`` (mandatory): a string providing the version of the bundle.
* ``shortTag`` (optional): a string providing the short tag for the bundle.
* ``category`` (optional): a string providing the category name for the bundle.
* ``maintainer`` (optional): a string providing the maintainer for the bundle (if not provided, the user loginName will be used).
* ``website`` (optional): a string providing the website URL for the bundle or maintainer.
* ``restrictionRule`` (optional): a string which indicates the "restriction rule" for a bundle. A restriction rule lists which distributions and/or target formats the bundle is designed for.
* ``sourceLogo`` (optional): a string providing the location of where to get the file. This can be a filesystem path (absolute or relative) or an URL.

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
	- name: "wordpress"
	  version: "3.5"
	  destination: "/tmp/wordpress"
	  maintainer: "wordpress"
	  files:
	  - # add files definition here  (see :ref:`stack-bundle-files` sub-section)
	- name: "wordpress language pack"
	  version: "3.5"
	  destination: "/tmp/wordpress"
	  maintainer: "wordpress"
	  files:
	  - # add files definition here  (see :ref:`stack-bundle-files` sub-section)


If you are using JSON:

.. code-block:: javascript

	{
	  "bundles": [
	    {
	      "name": "wordpress",
	      "version": "3.5",
	      "destination": "/tmp/wordpress",
	      "maintainer": "wordpress",
	      "files": [
	          ...add files definition here (see :ref:`stack-bundle-files` sub-section)
	      ]
	    },
	    {
	      "name": "wordpress language pack",
	      "version": "3.5",
	      "destination": "/tmp/wordpress",
	      "maintainer": "wordpress",
	      "files": [
	          ...add files definition here (see :ref:`stack-bundle-files` sub-section)
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
	- name: "wordpress"
	  version: "3.5"
	  description: "The wordpress files from wordpress.org"
	  destination: "/tmp/wordpress"
	  maintainer: "wordpress"
	  files:
	  - # add files definition here (see :ref:`stack-bundle-files` sub-section)
	  license:
	  - # add license definition here (see :ref:`stack-bundle-license` sub-section)

If you are using JSON:

.. code-block:: javascript

	{
	  "bundles": [
	    {
	      "name": "wordpress",
	      "version": "3.5",
	      "description": "The wordpress files from wordpress.org",
	      "destination": "/tmp/wordpress",
	      "maintainer": "wordpress",
	      "files": [
	          ...add files definition here (see :ref:`stack-bundle-files` sub-section)
	      ],
	      "license": {
	          ...add license definition here (see :ref:`stack-bundle-license` sub-section)
	      }
	    }
	  ]
	}

Adding a Website, Category and sourceLogo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example show how you can add website, category and logo information to the bundle.

If you are using YAML:

.. code-block:: yaml

	---
	bundles:
	- name: "wordpress"
	  version: "3.5"
	  description: "The wordpress files from wordpress.org"
	  destination: "/tmp/wordpress"
	  maintainer: "wordpress"
	  website: "https://fr.wordpress.org/"
	  category: "Blogging"
	  files:
	  - # add files definition here (see :ref:`stack-bundle-files` sub-section)
	  license:
	  - # add license definition here (see :ref:`stack-bundle-license` sub-section)
	  sourceLogo: "/tmp/wordpress.png"

If you are using JSON:

.. code-block:: javascript

	{
	  "bundles": [
	    {
	      "name": "wordpress",
	      "version": "3.5",
	      "description": "The wordpress files from wordpress.org",
	      "destination": "/tmp/wordpress",
	      "maintainer": "wordpress",
	      "website": "https://fr.wordpress.org/",
	      "category": "Blogging",
	      "files": [
	          ...add files definition here (see :ref:`stack-bundle-files` sub-section)
	      ],
	      "license": {
	          ...add license definition here (see :ref:`stack-bundle-license` sub-section)
	      },
	      "sourceLogo": "/tmp/wordpress.png"
	    }
	  ]
	}

To get the list of categories available, run command:

.. code-block:: shell

	$ hammr bundle categories

Adding Restriction Rules
~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows how you can set rules to restriction the bundle to specific distributions and/or target formats.
For a list of supported distribution and/or target formats refer to :ref:`command-line-os` and/or :ref:`command-line-os`.

The restriction rule is represented by a ``logical`` expression.
The format of simple expression is:  ``Object#field=value`` or ``Object#field!=value``.

   * object is ``Distribution`` or ``TargetFormat``
   * field is ``family``, ``pkgType``, ``name``, ``version`` or ``arch`` for Distribution object (see :ref:`command-line-os` and os list command to find values for field)
   * field is ``name`` or ``type`` for TargetFormat object (refer to :ref:`template-builders` section to get values for ``name`` field. Values for ``type`` field are cloud, virtual, physical or container)
   * value is the value you want to match with the fields (e.g. CentOS for Distribution name, linux for Distribution family, x86_64 for Distribution arch, VirtualBox for TargetFormat name, cloud for TargetFormat type...)
   * logical operator is ``||`` for OR and ``&&`` for AND
   * carriage return is not authorized

In the following example, the bundle is designed for (CentOS 6 x86_64 or CentOS 7 x86_64) or (all distribution if image is generated for VirtualBox)

If you are using YAML:

.. code-block:: yaml

	---
	bundles:
	- name: "wordpress"
	  version: "3.5"
	  description: "The wordpress files from wordpress.org"
	  destination: "/tmp/wordpress"
	  maintainer: "wordpress"
	  website: "https://fr.wordpress.org/"
	  category: "Blogging"
	  restrictionRule: "(Distribution#name=CentOS && Distribution#arch=x86_64 && (Distribution#version=7 || Distribution#version=6)) || TargetFormat#name=VirtualBox"
	  files:
	  - # add files definition here (see :ref:`stack-bundle-files` sub-section)
	  license:
	  - # add license definition here (see :ref:`stack-bundle-license` sub-section)
	  sourceLogo: "/tmp/wordpress.png"

If you are using JSON:

.. code-block:: javascript

	{
	  "bundles": [
	    {
	      "name": "wordpress",
	      "version": "3.5",
	      "description": "The wordpress files from wordpress.org",
	      "destination": "/tmp/wordpress",
	      "maintainer": "wordpress",
	      "website": "https://fr.wordpress.org/",
	      "category": "Blogging",
	      "restrictionRule" : "(Distribution#name=CentOS && Distribution#arch=x86_64 && (Distribution#version=7 || Distribution#version=6)) || TargetFormat#name=VirtualBox",
	      "files": [
	          ...add files definition here (see :ref:`stack-bundle-files` sub-section)
	      ],
	      "license": {
	          ...add license definition here (see :ref:`stack-bundle-license` sub-section)
	      },
	      "sourceLogo": "/tmp/wordpress.png"
	    }
	  ]
	}

Adding Third Party Software
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Within a template, you can include your own software and licenses, including bootscripts. The following is an example stack which uploads x file to a template

If you are using YAML:

.. code-block:: yaml

	---
	bundles:
	- name: "wordpress"
	  version: "3.5"
	  description: "The wordpress files from wordpress.org"
	  destination: "/tmp/wordpress"
	  maintainer: "wordpress"
	  website: "https://fr.wordpress.org/"
	  category: "Blogging"
	  restrictionRule: "Distribution#name=CentOS && Distribution#arch=x86_64 && Distribution#version=7"
	  files:
	  - name: "filename1.zip"
	    ownerGroup: "root:root"
	    rights: "755"
	    symlink: "/tmp/filename1_symlink.zip"
	    tag: "softwarefile"
	    source: "/usr/local/folder/filename1.zip"
	    md5sum: "1367cd10d6ce432cc44b4dc4bb2c4b01"
	    sha256sum: "72bc4caf81f5d9943ba32bf9703262e71ac256ca0308dfdbcc3c0b78a5d01cd4"
	    files: []
	  - name: "filename2.txt"
	    ownerGroup: "root:root"
	    rights: "755"
	    tag: "softwarefile"
	    source: "/usr/local/folder/filename2.txt"
	    files: []
	  - name: "iotop-0.6-2.el7.noarch.rpm"
	    tag: "ospkg"
	    source: "/usr/local/folder/iotop-0.6-2.el7.noarch.rpm"
	    files: []
	  - name: "bootscriptMysoftware.sh"
  	    bootOrder: 1
  	    bootType: "firstboot"
  	    tag: "bootscript"
  	    source: "/usr/local/folder/bootscriptMysoftware.sh"
  	    install: true
  	    md5sum: "a510c417e546c67a61c720a3696ef87c"
  	    sha256sum: "a7ae23c18a84338e9425a68a72c1b7cf66ea6ed30bd142ee0a824d6bf02e67e1"
  	    files: []
	  license:
	  - # add license definition here (see :ref:`stack-bundle-license` sub-section)
	  sourceLogo: "/tmp/wordpress.png"

If you are using JSON:

.. code-block:: javascript

	{
	  "bundles": [
	    {
	      "name": "wordpress",
	      "version": "3.5",
	      "description": "The wordpress files from wordpress.org",
	      "destination": "/tmp/wordpress",
	      "maintainer": "wordpress",
	      "website": "https://fr.wordpress.org/",
	      "category": "Blogging",
	      "restrictionRule" : "Distribution#name=CentOS && Distribution#arch=x86_64 && Distribution#version=7",
	      "files": [{
		  	"name": "filename1.zip",
		  	"ownerGroup" : "root:root",
		  	"rights" : "755",
		  	"symlink" : "/tmp/filename1_symlink.zip",
		  	"tag" : "softwarefile",
		  	"source": "/usr/local/folder/filename1.zip",
		  	"files" : [ ]
		  }, {
		  	"name": "filename2.txt",
		  	"ownerGroup" : "root:root",
		  	"rights" : "755",
		  	"tag" : "softwarefile",
		  	"source": "/usr/local/folder/filename2.txt",
		  	"files" : [ ]
		  }, {
		  	"name" : "iotop-0.6-2.el7.noarch.rpm",
		  	"tag" : "ospkg",
		  	"source" : "/usr/local/folder/iotop-0.6-2.el7.noarch.rpm",
		  	"files" : [ ]
		  }, {
		  	"name" : "bootscriptMysoftware.sh",
		  	"bootOrder" : 1,
		  	"bootType" : "firstboot",
		  	"tag" : "bootscript",
		  	"source" : "/usr/local/folder/bootscriptMysoftware.sh",
		  	"install" : true,
		  	"md5sum" : "a510c417e546c67a61c720a3696ef87c",
		  	"sha256sum" : "a7ae23c18a84338e9425a68a72c1b7cf66ea6ed30bd142ee0a824d6bf02e67e1",
		  	"files" : [ ]
	      } ],
	      "license": {
	          ...add license definition here (see :ref:`stack-bundle-license` sub-section)
	      },
	      "sourceLogo": "/tmp/wordpress.png"
	    }
	  ]
	}
