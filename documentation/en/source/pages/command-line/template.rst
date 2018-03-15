.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _command-line-template:

template
========

Manages all the templates created by the user. The usage is:

.. code-block:: shell

	usage: hammr template [sub-command] [options]


Sub Commands
------------

``build`` sub-command
~~~~~~~~~~~~~~~~~~~~~

Builds a machine image from the template. The options are:

	* ``--file`` (mandatory): json or yaml file providing the builder parameters

``clone`` sub-command
~~~~~~~~~~~~~~~~~~~~~

Clones the template. The clone is copying the meta-data of the template. The options are:

	* ``--id`` (mandatory): the ID of the template to clone
	* ``--name`` (mandatory): the name to use for the new cloned template
	* ``--version`` (mandatory): the version to use for the cloned template

``create`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Creates a new template and saves it to the UForge server. Hammr creates a tar.gz archive which includes the JSON or YAML file and binaries, and imports it to UForge. The options are:

	* ``--file`` (mandatory): json or yaml file containing the template content
	* ``--archive-path`` (optional): path of where to store the archive (tar.gz) of the created template. If provided, hammr creates an archive of the created template, equivalent to running ``template export``
	* ``--force`` (optional): force template creation (delete template/bundle if already exist)
	* ``--rbundles`` (optional): if a bundle already exists, use it in the new template. Warning: this option ignore the content of the bundle described in the template file
	* ``--usemajor`` (optional): use distribution major version if exit

``delete`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Deletes an existing template. The options are:

	* ``--id`` (mandatory): the ID of the template to delete

``export`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Exports a template by creating an archive (compressed tar file) that includes the JSON or YAML configuration file. The options are:

	* ``--id`` (mandatory): the ID of the template to export
	* ``--file`` (optional): destination path where to store the template configuration file on the local filesystem
	* ``--outputFormat`` (optional): output format (yaml or json) of the template file to export (yaml is the default one)

``import`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Creates a template from an archive. The archive file must be a tar.gz (which includes the .json or yaml, and binaries). The options are:

	* ``--file`` (mandatory): the path of the archive
	* ``--force`` (optional): force template creation (delete template/bundle if already exist)
	* ``--usemajor`` (optional): use distribution major version if exit

``list`` sub-command
~~~~~~~~~~~~~~~~~~~~

Displays all the created templates.

``validate`` sub-command
~~~~~~~~~~~~~~~~~~~~~~~~

Validates the syntax of a template configuration file. The options are:

	* ``--file`` (mandatory): the json or yaml configuration file
