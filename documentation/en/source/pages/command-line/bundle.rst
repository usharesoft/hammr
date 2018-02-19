.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _command-line-bundle:

bundle
======

Manages all the bundles that have been registered in UForge. A bundle is group of software that is uploaded during the creation of a template. The usage is:

.. code-block:: shell

	usage: hammr bundle [sub-command] [options]

Sub Commands
------------

``categories`` sub-command
~~~~~~~~~~~~~~~~~~~~~~~~~~

Lists all the categories available for bundles.

``clone`` sub-command
~~~~~~~~~~~~~~~~~~~~~

Clones the bundle. The clone is copying the meta-data of the bundle. The options are:

	* ``--id`` (mandatory): the ID of the bundle to clone
	* ``--name`` (mandatory): the name to use for the new cloned bundle
	* ``--version`` (mandatory): the version to use for the cloned bundle

``create`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Creates a new bundle and saves it to the UForge server. Hammr creates a tar.gz archive which includes the .json or .yml file and binaries and imports it to UForge. The options are:

	* ``--file`` (mandatory): json or yaml file containing the bundle content. See the :ref:`stack-bundle-files` sub-section for available keys.
	* ``--archive-path`` (optional): path of where to store the archive (tar.gz) of the created bundle. If provided, hammr creates an archive of the created bundle, equivalent to running ``bundle export``

``delete`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Deletes an existing bundle. The options are:

	* ``--id`` (mandatory): the ID of the bundle to delete

``export`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Exports a bundle by creating an archive (compressed tar file) that includes the .json or .yml bundle configuration file. The options are:

	* ``--id`` (mandatory): the ID of the bundle to export
	* ``--file`` (optional): destination path where to store the bundle configuration file on the local filesystem
	* ``--outputFormat`` (optional): output format (yaml or json) of the bundle file to export (yaml is the default one)

``import`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Creates a bundle from an archive. The archive file must be a tar.gz (which includes the .json or .yml and binaries). The options are:

	* ``--file`` (mandatory): the path of the archive

``list`` sub-command
~~~~~~~~~~~~~~~~~~~~

Lists all the bundles that have been registered in the UForge server.

``validate`` sub-command
~~~~~~~~~~~~~~~~~~~~~~~~

Validates the syntax of a bundle configuration file. The options are:

	* ``--file`` (mandatory): the json or yaml configuration file