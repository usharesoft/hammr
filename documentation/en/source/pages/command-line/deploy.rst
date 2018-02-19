.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _command-line-deploy:

deploy
======

Manages all your deployments. The usage is:

.. code-block:: shell

	usage: hammr deploy [sub-command] [options]


Sub Commands
------------

``list`` sub-command
~~~~~~~~~~~~~~~~~~~~

Displays all the deployments and information about their respective target platforms.

``terminate`` sub-command
~~~~~~~~~~~~~~~~~~~~~~~~~

Terminates a deployment. The options are:

	* ``--id`` (mandatory): the ID of the deployment to terminate
        * ``--force`` (optional): terminates the deployment without asking for confirmation
