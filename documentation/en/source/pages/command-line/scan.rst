.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _command-line-scan:

scan
====

Manages all the scans executed on live systems. The usage is:

.. code-block:: shell

	usage: hammr scan [sub-command] [options]


Sub Commands
------------

``build`` sub-command
~~~~~~~~~~~~~~~~~~~~~

Builds a machine image from a scan. The options are:

	* ``--id`` (mandatory): the ID of the scan to generate the machine image from
	* ``--file`` (mandatory): json or yaml file providing the builder parameters

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` and ``hardwareSettings`` section in ``builders``. Refer to :ref:`stack-installation` for installation details and :ref:`template-builders` for the hardware settings, which depend on the builder type.


``delete`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Deletes an existing scan. The options are:

	* ``--id`` (mandatory): the ID of the instance or scan to delete
	* ``--scantype`` (mandatory): the type to be deleted. Can be one of: instance, scan, or all. When you set the type to ``instance``, the instance and all scans linked to it will be deleted unless using the ``scansonly`` flag. When you specify the type as ``scan`` only the scan with the ID to specify will be deleted. If you set the type to ``all``, all the instances and scans on your UForge will be deleted (regardeless of the ``id`` you set).
	* ``--scansonly`` (optional): this flag can be used when the scan type is set to ``instance``. In this case, only the scans linked to the specified instance will be deleted (not the instance itself).

``import`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Imports (or transforms) the scan to a template.

	* ``--id`` (mandatory): the ID of the scan to import
	* ``--name`` (mandatory): the name to use for the template created from the scan
	* ``--version`` (mandatory): the version to use for the template created from the scan

``list`` sub-command
~~~~~~~~~~~~~~~~~~~~

Displays all the scans for the user.

``run`` sub-command
~~~~~~~~~~~~~~~~~~~

Executes a deep scan of a running system.

	* ``--ip`` (mandatory): the IP address or fully qualified hostname of the running system
	* ``--scan-login`` (mandatory): the root user name (normally root)
	* ``--name`` (mandatory): the scan name to use when creating the scan meta-data
	* ``--scan-password`` (optional): the root password to authenticate to the running system
	* ``--dir`` (optional): the directory where to install the uforge-scan.bin binary used to execute the deep scan
	* ``--exclude`` (optional): a list of directories or files to exclude during the deep scan
	* ``--overlay`` (optional): include overlay (extra files) for the given scan

.. note:: If a CTR exception (eg: `ERROR: Caught exception: CTR mode needs counter parameter, not IV`) occurs while executing ``run`` sub-command try upgrading your paramiko library to either 1.18.4 or 2.3.1 using ``sudo pip install paramiko==VERSION``.