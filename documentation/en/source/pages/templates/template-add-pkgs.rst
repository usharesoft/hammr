.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _template-add-pkgs:

Adding Packages to Your Template
================================

When defining your machine image you set the OS and profile. UForge automatically pulls in all the necessary packages required for the chosen OS. You do not need to list them seperately. However, you may want to add other packages to your machine image. These additional packages are listed in the ``pkgs`` section of your template.

.. note:: If the packages you choose to add to your template have any dependencies, all the required packages will be added automatically.  You do not have to search and list all the dependencies in your template.


The following is a basic example for a CentOS 6.4 32-bit template with package for ``iotop`` added, when using YAML.

.. code-block:: yaml

	---
	os:
	  name: CentOS
	  version: '6.4'
	  arch: x86_64
	  profile: Minimal
	  pkgs:
	  	name: iotop

If you are using JSON:

.. code-block:: json

	{
	    "os" : {
	      "name" : "CentOS",
	      "version" : "6.4",
	      "arch" : "x86_64",
	      "profile" : "Minimal"
	      "pkgs" : {
	        "name" : "iotop"
	      }
	    }
	}