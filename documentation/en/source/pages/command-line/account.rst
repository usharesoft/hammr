.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _command-line-account:

account
=======

Manages all of your different cloud accounts used when either building or publishing machine images. The usage is:

.. code-block:: shell

	usage: hammr account [sub-command] [options]


Sub Commands
------------

``create`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Creates a new cloud account. The options are:

	* ``--file`` (mandatory): json or yaml file providing the cloud account parameters

``delete`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Deletes an existing cloud account. The options are:

	* ``--id`` (mandatory): the ID of the cloud account to delete

``list`` sub-command
~~~~~~~~~~~~~~~~~~~~

Displays all the cloud accounts for the user.