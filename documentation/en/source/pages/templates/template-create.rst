.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _template-create:

Creating a Template
===================

A template is a configuration file which defines the machine image you want to build. The format of this file is either JSON or YAML. Note that the template can be saved locally or stored on a server, in which case hammr will access it via a URL. For security reasons we recommend that you save your UForge credentials in a seperate credentials file, saved at the same location as your template.

The mandatory values when creating a template are:

	* ``name``: the name of the template to create. You can easily make the name unique by using the timestamp keyword (surrounded by curly brackets).
	* ``version``: the version of the template.
	* ``os`` : the operating system details to use the in your images. You must include the OS family name, version and architecture type. For more information regarding OS and package parameters, see :ref:`template-add-pkgs`
	
For more details about the various parameters you can set in your template to define the machine image you want to create, refer to the :ref:`templates-spec` section.

The following is an example of the minimum information needed in your configuration file to define a template. It includes the name, version, a few installation parameters and the OS. The following YAML example describes a CentOS 6.4 32-bit template. JSON can also be used.

.. code-block:: yaml

	---
	stack:
	  name: myTemplate
	  version: '1.0'
	  installation:
	    internetSettings: basic
	    diskSize: 12288
	    swapSize: 512
	  os:
	    name: CentOS
	    version: '6.4'
	    arch: x86_64
	    profile: Minimal

If you are using JSON:

.. code-block:: json

	{
	  "stack" : {
	    "name" : "myTemplate",
	    "version" : "1.0",
	    "installation" : {
	      "internetSettings" : "dhcp",
	      "diskSize" : 12288,
	      "swapSize" : 512
	    },
	    "os" : {
	      "name" : "CentOS",
	      "version" : "6.4",
	      "arch" : "x86_64",
	      "profile" : "Minimal"
	    }
	 }
	}

Once you have written and saved the minimal template you can then create the template using ``template create``:

.. code-block:: shell

	$ hammr template create --file <blueprint>.yml
	Validating the template file [/Users/james/nginx-template.yml] ...
	OK: Syntax of template file [/Users/james/nginx-template.yml] is ok
	Creating template from temporary [/var/folders/f6/8kljm7cx3h7fvb26tq18kw4m0000gn/T/hammr-15888/archive.tar.gz] archive ...
	100%|#############################################################################|
	OK: Template create: DONE
	Template URI: users/root/appliances/898
	Template Id : 898

