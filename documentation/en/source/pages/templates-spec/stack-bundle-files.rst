.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-bundle-files:

files
=====

Within a ``bundle``, the ``files`` sub-section describes the list of files, binaries, archives or native packages that are part of the bundle. Within the ``files`` you can also list a folder.

.. note:: If you list a folder in ``files`` sub-section, it can have its own ``files`` sub-section to provide more information for a specific file in the folder (i.e. rights, owner:group, symlink etc)

The definition of a ``files`` section when using YAML is:

.. code-block:: yaml

	---
	files:
	- # the list of files goes here.

If you are using JSON:

.. code-block:: javascript

	{
		"files": [
		    ...the list of files goes here.
		]
	}

The valid keys to use within a file are:

* ``destination`` (optional): a string providing the destination path where to install the file on the machine image filesystem. This overrides any destination install path provided in the bundle section.
* ``ownerGroup`` (optional): a string corresponding to the owner:group to set during generation for the file (tag key must be equals to softwarefile. If not provided, "root:root" will be used by default).
* ``rights`` (optional): a string corresponding to the rights (i.e. 755) to set during generation for the file (tag key must be equals to softwarefile. If not provided, "755" will be used by default).
* ``symlink`` (optional): a string providing the location of the symlink to create during generation for the file (tag key must be equals to softwarefile).
* ``bootOrder`` (optional): an integer providing the boot order. (tag key must be equals to bootscript).
* ``bootType`` (optional): a string providing the script type, firstboot or everyboot (tag key must be equals to bootscript).
* ``tag`` (optional): a string describing the type of the file provided (softwarefile, ospkg or bootscript). ospkg and bootscript can only be in the first level files section (if not provided, the file will be considered as a softwarefile)
* ``extract`` (optional): a boolean describing whether to uncompress/extract the archive file during the build process. This flag can only be used if the file is an archive, otherwise this flag is ignored.
* ``install`` (optional): a boolean describing whether to install the native package as part of the build. It can only be used for native packages. If false, then the native package will be added to the filesystem as a file described by the destination. Otherwise the package will be treated like any other native package – package dependencies will be verified and installed. If the file is not a native package then this flag is ignored.
* ``md5sum`` (optional): a string providing a md5sum checksum.
* ``name`` (mandatory): a string providing the name of the bundle.
* ``params`` (optional): a string providing any parameters to execute with the binary file as part of the generation process. These parameters are ignored if the file is not a binary (.msi, .exe etc)
* ``source`` (mandatory): a string providing the location of where to get the file. This can be a filesystem path (absolute or relative) or an URL.
* ``files`` (optional): an array of objects describing the files, archives or packages contained in the file representing a folder (file must represents a folder and tag key must be equals to softwarefile and all files in it can only be tagged as softwarefile).

Examples
--------

Basic Example
~~~~~~~~~~~~~

The following example shows how to declare a set of files to uploaded as part of a bundle.

If you are using YAML:

.. code-block:: yaml

	---
	files:
	- name: wordpress.zip
	  source: http://wordpress.org/wordpress-3.5.zip

If you are using JSON:

.. code-block:: json

	{
	  "files": [
	    {
	      "name": "wordpress.zip",
	      "source": "http://wordpress.org/wordpress-3.5.zip"
	    }
	  ]
	}

Example of a Folder in Files Sub-section
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows how to declare a folder to be uploaded as part of a bundle. All the files within the declared bundle will be uploaded.

.. note:: You cannot upload the same source folder with two different names. In the end, the source folder and files will only be uploaded once.

If you are using YAML:

.. code-block:: yaml

	---
	files:
	- name: folder
	  source: "/usr/local/folder"

If you are using JSON:

.. code-block:: json

      {
        "files": [
          {
            "name": "folder",
            "source": "/usr/local/folder"
          }
        ]
      }

Example of a Folder in Files Sub-section with its own Files Sub-section
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example shows how to declare a folder to be uploaded as part of a bundle. All the files within the declared bundle will be uploaded.
A folder can have a Files Sub-section to to add more information for a file in it like rights, owner:group etc.

.. note:: You cannot upload the same source folder with two different names. In the end, the source folder and files will only be uploaded once.

If you are using YAML:

.. code-block:: yaml

	---
	  files:
	  - name: "folder"
	  	tag: "softwarefile"
	  	source: "/usr/local/folder"
	  	files:
	  	- name: "filename1.zip"
		  ownerGroup: "root:root"
		  rights: "755"
		  symlink: "/tmp/filename1_symlink.zip"
		  tag: "softwarefile"
		  source: "/usr/local/folder/filename1.zip"
		  files: []
		- name: "folder2"
		  ownerGroup: "root:root"
		  rights: "765"
		  tag: "softwarefile"
		  source: "/usr/local/folder/folder2"
		  files:
		  - name: "folder3"
		    ownerGroup: "root:root"
		    rights: "755"
		    symlink: "/tmp/folder3_symlink"
		    tag: "softwarefile"
		    source: "/usr/local/folder/folder2/folder3"
		    files: [
			- name: "filename3.zip"
			  ownerGroup: "root:root"
			  rights: "765"
			  tag: "softwarefile"
			  source: "/usr/local/folder/folder2/folder3/filename3.zip"
			  files: []

If you are using JSON:

.. code-block:: json

      {
        "files": [
          {
            "name": "folder",
            "tag" : "softwarefile",
            "source": "/usr/local/folder",
            "files": [
			  {
				"name": "filename1.zip",
				"ownerGroup" : "root:root",
				"rights" : "755",
				"symlink" : "/tmp/filename1_symlink.zip",
			  	"tag" : "softwarefile",
				"source": "/usr/local/folder/filename1.zip",
				"files" : [ ]
			  },
			  {
				"name": "folder2",
				"ownerGroup" : "root:root",
				"rights" : "765",
				"tag" : "softwarefile",
				"source": "/usr/local/folder/folder2",
				"files": [
				  {
					"name": "folder3",
					"ownerGroup" : "root:root",
					"rights" : "755",
					"symlink" : "/tmp/folder3_symlink",
					"tag" : "softwarefile",
					"source": "/usr/local/folder/folder2/folder3",
					"files": [
					  {
						"name": "filename3.zip",
						"ownerGroup" : "root:root",
						"rights" : "765",
						"tag" : "softwarefile",
						"source": "/usr/local/folder/folder2/folder3/filename3.zip",
						"files" : [ ]
					  }
					]
				  }
				]
			  }
			]
          }
        ]
      }

Overriding Bundle Destination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The bundle via destination provides the global install path for all the files. This example shows how you can add a file to another directory in the filesystem, effectively overriding the default destination directory.

If you are using YAML:

.. code-block:: yaml

	---
	files:
	- name: wordpress.zip
	  source: http://wordpress.org/wordpress-3.5.zip
	  destination: "/usr/local/wordpress"

If you are using JSON:

.. code-block:: json

	{
	  "files": [
	    {
	      "name": "wordpress.zip",
	      "source": "http://wordpress.org/wordpress-3.5.zip",
	      "destination": "/usr/local/wordpress"
	    }
	  ]
	}


Extracting Archives
~~~~~~~~~~~~~~~~~~~

The example uses the extract key to automatically extract the archive file:

If you are using YAML:

.. code-block:: yaml

	---
	files:
	- name: wordpress.zip
	  source: http://wordpress.org/wordpress-3.5.zip
	  destination: "/usr/local/wordpress"
	  extract: true

If you are using JSON:

.. code-block:: json

	{
	  "files": [
	    {
	      "name": "wordpress.zip",
	      "source": "http://wordpress.org/wordpress-3.5.zip",
	      "destination": "/usr/local/wordpress",
	      "extract": true
	    }
	  ]
	}

Installing or Placing Native Packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The example declares a native package to be added to the bundle. The install key is used to tell the build process not to install the package, but to add it to the filesystem in the destination directory.

If you are using YAML:

.. code-block:: yaml

	---
	files:
	- name: "mypackage.rpm"
	  source: "/home/joris/demo/mypackage-3.1.rpm"
	  destination: "/usr/local/rpms"
	  tag: "softwarefile"
	  install: false

If you are using JSON:

.. code-block:: json

	{
	  "files": [{
	      "name": "mypackage.rpm",
	      "source": "/home/joris/demo/mypackage-3.1.rpm",
	      "destination": "/usr/local/rpms",
		  "tag" : "softwarefile",
	      "install": false
	    }
	  ]
	}

If install is set to ``true``, then the package is installed as a native package (including package dependency checking) and then destination information is ignored.

.. note:: A native package is different than a repository package. See next example for the differences


Introduced simple file, repository package and bootscript
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The example declares a repository package, a bootscript and a file to be added to the bundle. The tag key is used to tell what kind of file the section represents (if tag is not specified, it will be considered as a simple file to be uploaded).

If you are using YAML:

.. code-block:: yaml

	---
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

If you are using JSON:

.. code-block:: json

	{
	  "files": [{
		  "name": "filename1.zip",
		  "ownerGroup" : "root:root",
		  "rights" : "755",
		  "symlink" : "/tmp/filename1_symlink.zip",
		  "tag" : "softwarefile",
		  "source": "/usr/local/folder/filename1.zip",
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
	    }
	  ]
	}

The ``source`` section for a file tagged as ``ospkg`` must be here but can be a false source because it doesn't matter. The repository package will be searched by the distribution and the fullname
To get the fullname of a repository package, See the :ref:`pkgs-search`.
During export or create, a file tagged as ``ospkg`` will be search by fullname in the unique distribution given in ``oses`` section of the bundle.

Using Parameters for Binaries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The example declares a binary file to be added to the bundle. The params key is used to provide a set of parameters that are used to execute the binary.

If you are using YAML:

.. code-block:: yaml

	---
	files:
	- name: mybinary.exe
	  source: "/home/joris/demo/mybinary.exe"
	  params: "--silent"

If you are using JSON:

.. code-block:: json

	{
	  "files": [
	    {
	      "name": "mybinary.exe",
	      "source": "/home/joris/demo/mybinary.exe",
	      "params": "--silent"
	    }
	  ]
	}

.. warning:: Hammr only supports windows binaries to be executed with parameters (.exe and .msi). For linux, use the :ref:`stack-config` section to declare boot scripts.