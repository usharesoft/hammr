.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _export-template:

Exporting a Template
====================

To illustrate exporting a template, let’s start from scratch. We will create a template, get the ID and export it with hammr.

So first lets create a new template with the YAML file ``centoscore-template.yml``.

.. note:: You can also use JSON.

.. code-block:: yaml

	---
	stack:
	  name: CentOS Core
	  version: '6.4'
	  os:
	    name: CentOS
	    version: '6.4'
	    arch: x86_64
	    profile: Minimal
	  config:
	  - name: firstboot1.sh
	    source: http://myconfig.site.com/config/firstboot1.sh
	    type: bootscript
	    frequency: firstboot
	  - name: firstboot0.sh
	    source: http://myconfig.site.com/config/firstboot1.sh
	    type: bootscript
	    frequency: firstboot

If you are using JSON:

.. code-block:: json

	{
	  "stack" : {
	    "name" : "CentOS Core",
	    "version" : "6.4",
	    "os" : {
	      "name" : "CentOS",
	      "version" : "6.4",
	      "arch" : "x86_64"
	      "profile" : "Minimal"
	    },
	    "config" : [ {
	      "name" : "firstboot1.sh",
	      "source" : "http://myconfig.site.com/config/firstboot1.sh",
	      "type" : "bootscript",
	      "frequency" : "firstboot"
	    }, {
	      "name" : "firstboot0.sh",
	      "source" : "http://myconfig.site.com/config/firstboot1.sh",
	      "type" : "bootscript",
	      "frequency" : "firstboot"
	    } ]
	  }
	}

.. code-block:: shell

	$ hammr template create --file centoscore-template.yml

Now that the template is created we need to get the ``Id`` of the template you want to export. To do so, list the templates with the command ``template list``:

.. code-block:: shell

	$ hammr template list
	+-----+------------------------------+---------+---------------------+---------------------+---------------------+--------+---------+-----+--------+
	| Id  |             Name             | Version |         OS          |       Created       |    Last modified    | # Imgs | Updates | Imp | Shared |
	+=====+==============================+=========+=====================+=====================+=====================+========+=========+=====+========+
	| 669 | CentOS Core                  | 1.0     | CentOS 6.4 x86_64   | 2014-04-25 13:55:19 | 2014-05-09 13:24:59 | 0      | 0       |     |        |
	+-----+------------------------------+---------+---------------------+---------------------+---------------------+--------+---------+-----+--------+

In this case the ``Id`` is ``669``. To export the template, run the command ``template export``:

.. code-block:: shell

	$ hammr template export --id 669 --file /tmp/centos-core-archive.tar.gz
	Exporting template with id [669] :
	100%|#################################################################################|
	Downloading archive...
	OK: Download complete of file [/tmp/centos-core-archive.tar.gz]

Now if you uncompress the archive, you will find a file ``template.yml``, which is the template YAML configuration file and a sub-directory ``config`` containing the two boot scripts.

.. note:: If the command ``template export`` has ``--outputFormat json`` argument, the file ``template.yml`` in the result archive will be replaced by file ``template.json``.

If you open the ``template.yml`` file, then you will notice that there is additional information added, including:

* ``pkgs``: this contains all the packages that are added by the os profile ``Minimal``
* ``updateTo``: this is the date that the template initially created. This ensures that if you re-import this template (the creation date might be different) and build a machine image, the machine image will be identical to any machine image built from the original template
* ``installation``: adds the default installation parameters.
