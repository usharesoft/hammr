.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _stack-bundle-files:

files
=====

Within a ``bundle``, the ``files`` sub-section describes the list of files, binaries, archives or native packages that are part of the bundle. Within the ``files`` you can also list a folder.

The definition of a files section is:

.. code-block:: javascript

	{
		"files": [
		    ...the list of files goes here.
		]
	}

The valid keys to use within a file are:

* ``destination`` (optional): a string providing the destination path where to install the file on the machine image filesystem. This overrides any destination install path provided in the bundle section.
* ``extract`` (optional): a boolean describing whether to uncompress/extract the archive file during the build process. This flag can only be used if the file is an archive, otherwise this flag is ignored.
* ``install`` (optional): a boolean describing whether to install the native package as part of the build. It can only be used for native packages. If false, then the native package will be added to the filesystem as a file described by the destination. Otherwise the package will be treated like any other native package – package dependencies will be verified and installed. If the file is not a native package then this flag is ignored.
* ``md5sum`` (optional): a string providing a md5sum checksum.
* ``name`` (mandatory): a string providing the name of the bundle.
* ``params`` (optional): a string providing any parameters to execute with the binary file as part of the generation process. These parameters are ignored if the file is not a binary (.msi, .exe etc)
* ``source`` (mandatory): a string providing the location of where to get the file. This can be a filesystem path (absolute or relative) or an URL.

Examples
--------

Basic Example
~~~~~~~~~~~~~

The following example shows how to declare a set of files to uploaded as part of a bundle.

.. note:: If you declare the same file twice, the second file will overwrite the first one.

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

.. code-block:: json

      {
        "files": [
          {
            "name": "folder",
            "source": "/usr/local/folder"
          }
        ]
      }


Overriding Bundle Destination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The bundle via destination provides the global install path for all the files. This example shows how you can add a file to another directory in the filesystem, effectively overriding the default destination directory.

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

.. code-block:: json

	{
	  "files": [{
	      "name": "mypackage.rpm",
	      "source": "/home/joris/demo/mypackage-3.1.rpm",
	      "destination": "/usr/local/rpms",
	      "install": false
	    }
	  ]
	}

If install is set to ``true``, then the package is installed as a native package (including package dependency checking) and then destination information is ignored.

Using Parameters for Binaries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The example declares a binary file to be added to the bundle. The params key is used to provide a set of parameters that are used to execute the binary.

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