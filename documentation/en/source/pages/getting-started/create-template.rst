.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _create-template:

Creating the Template
=====================

A configuration file, named the template, defines the contents of the machine image and any credential information required to generate and publish the image to the target environment.

Lets create a template for the nginx machine image. Create a file ``nginx-template.yml`` with the following content.

.. note:: JSON can also be used.

.. code-block:: yaml

	---
	stack:
	  name: nginx
	  version: '1.0'
	  os:
	    name: Ubuntu
	    version: '12.04'
	    arch: x86_64
	    profile: Minimal
	    pkgs:
	    - name: nginx
	  installation:
	    diskSize: 12288

If you are using JSON:

.. code-block:: json

	{
		"stack": {
			"name": "nginx",
			"version": "1.0",
			"os": {
			    "name": "Ubuntu",
			    "version": "12.04",
			    "arch": "x86_64",
			    "profile": "Minimal",
			    "pkgs": [{
			        "name": "nginx"
			    }]
			},
			"installation": {
			    "diskSize": 12288
			}
		}
	}



A couple of things to point out at this stage. The ``stack`` section defines the content of the machine you want to build. There are many sub-sections (see the :ref:`template-stack` glossary), the:

	* ``os``: defines the operating system you want to use (in this case Ubuntu 12.04 64bit); the profile type (minimal); and any specific packages to install (nginx)
	* ``installation``: defines lower level installation parameters. In this example a disk size of 8GB

Now lets create the template using hammr. First lets validate that the configuration file does not have any syntax errors or missing mandatory values, by using the command ``template validate`` and passing in our template file ``nginx-template.yml`` (or .json file is you are using JSON).

.. code-block:: shell

	$ hammr template validate --file nginx-template.yml
	Validating the template file [/Users/james/nginx-template.yml] ...
	OK: Syntax of template file [/Users/james/nginx-template.yml] is ok

Now run the command ``template create``.

.. code-block:: shell

	$ hammr template create --file nginx-template.yml
	Validating the template file [/Users/james/nginx-template.yml] ...
	OK: Syntax of template file [/Users/james/nginx-template.yml] is ok
	Creating template from temporary [/var/folders/f6/8kljm7cx3h7fvb26tq18kw4m0000gn/T/hammr-15888/archive.tar.gz] archive ...
	100%|#############################################################################|
	OK: Template create: DONE
	Template URI: users/root/appliances/898
	Template Id : 898

This takes the information in the ``stack`` section of the template configuration file and stores this in the UForge server.

You can display all the templates created by using ``template list``.

.. code-block:: shell

	$ hammr template list
	+-----+----------------------+---------+---------------------+---------------------+---------------------+--------+---------+-----+--------+
	| Id  |         Name         | Version |         OS          |       Created       |    Last modified    | # Imgs | Updates | Imp | Shared |
	+=====+======================+=========+=====================+=====================+=====================+========+=========+=====+========+
	 683 | nginx                | 1.0     | Ubuntu 12.04 x86_64 | 2014-05-02 13:59:25 | 2014-05-02 13:59:27 | 0      | 0       |     |        |
	+-----+----------------------+---------+---------------------+---------------------+---------------------+--------+---------+-----+--------+
	Found 1 templates

You can create one or more machine images from this template.


