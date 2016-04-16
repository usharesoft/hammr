.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _command-line-bundle:

bundle
======

Manages all the bundles that have been registered in UForge. A bundle is group of software that is uploaded during the creation of a template. The usage is:

.. code-block:: shell

	usage: hammr bundle [sub-command] [options]

Sub Commands
------------

``delete`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Deletes an existing bundle. The options are:

	* ``--id`` (mandatory): the ID of the bundle to delete

``list`` sub-command
~~~~~~~~~~~~~~~~~~~~

Lists all the bundles that have been registered in the UForge server.