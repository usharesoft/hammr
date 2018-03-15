.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _import-template:

Importing a Template
====================

You can import a template based on a tar.gz archive file by using the command ``template import``. This will import the archive, which contains the JSON or YAML file and binaries of the template.

.. code-block:: shell

	$ hammr template import --file /tmp/centos-core-archive.tar.gz
	Importing template from [/tmp/centos-core-archive.tar.gz] archive ...
	100%|#################################################################################|
	OK: Template import: DONE
	Template URI: users/root/appliances/22
	Template Id : 22
