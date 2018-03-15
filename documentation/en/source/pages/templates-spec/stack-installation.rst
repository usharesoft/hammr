.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-installation:

installation
============

Within a :ref:`template-stack`, the ``installation`` sub-section describes questions that are normally related to the installation of an operating system. This includes root password, keyboard settings, timezone, and partitioning. These questions are only asked once as part of the operating system installation; consequently decided by the person when building machine images manually. Hammr provides a mechanism that allows some of the installation questions to be asked as part of the first-boot when provisioning an instance from the machine image. This makes any machine image built by hammr to be more flexible, for example if you have a team in the UK and another team in France then their keyboard settings are most likely to be QWERTY and AZERTY respectively. Allowing the end-user to choose the keyboard settings as part of first-boot can help resolve hours of frustration.

The definition of a ``pkgs`` section when using YAML is:

.. code-block:: yaml

	---
	installation:
	  # the installation definition goes here.

If you are using JSON:

.. code-block:: javascript

	"installation": {
	    ...the installation definition goes here.
	}

The valid keys to use within an installation are:

* ``diskSize`` (optional): an integer value (in MB) providing the disk size of the machine image. This value is ignored if an advanced partitioning table is provided (see :ref:`stack-installation-partitioning`)
* ``displayLicense`` (optional): a boolean value to display any EULA during the first boot of a provisioned instance (includes operating system EULA and any license information provided in the :ref:`stack-bundles` section of the stack). If the value is ``false`` then no license information is displayed. If ``displayLicense`` is not used, then by default all license information is displayed during first boot.
* ``internetSettings`` (optional): a string providing the network settings. Possible values ``basic``, ``ask`` or ``configure``. If no value is provided, is set to ``basic`` by default. Refer to the :ref:`stack-installation-internet` sub-section for more information.
* ``kernelParams`` (optional): an array of strings providing the kernel parameters to use. These parameters are used when provisioning an instance from the machine image. If no kernel parameters are provided, the ``rhbg`` and ``quiet`` parameters are set by default
* ``keyboard`` (optional): a string providing the keyboard layout to use. If no keyboard setting is provided, then during first boot the keyboard setting is prompted. See :ref:`stack-installation-keyboard` for all available values for keyboard
* ``partitioning`` (optional): an array of objects describing an advanced partitioning table. Refer to :ref:`stack-installation-partitioning` sub-section for more information.
* ``rootUser`` (optional): an object describing the configuration information of the root user (or primary administrator). If ``rootUser`` is not provided, then during first boot the root user password is prompted
* ``swapSize`` (optional): an integer value (in MB) providing the swap size to be allocated. This value is ignored if an advanced partitioning table is provided (see :ref:`stack-installation-partitioning`)
* ``timezone`` (optional): a string providing the timezone to use. If no timezone is provided, then during first boot the timezone is prompted. See :ref:`stack-installation-timezone` for all available values for timezone.
* ``firewall`` (optional): a boolean to enable or disable the firewall service. If no firewall is given, then the firewall is asked during installation.
* ``welcomeMessage`` (optional): a string providing a welcome message displayed during the first boot of a provisioned instance
* ``seLinuxMode`` (optional): a string indicating the SELinux mode (see :ref:`stack-installation-selinux`)


Sub-sections
------------

The ``installation`` sub-sections are:

.. toctree::
   :titlesonly:

   stack-installation-keyboard
   stack-installation-groups
   stack-installation-internet
   stack-installation-partitioning
   stack-installation-rootuser
   stack-installation-timezone
   stack-installation-users
   stack-installation-selinux


Example
-------

The following example sets the timezone, disk size, swap size, kernel parameters and automatically accepts all the licenses on the end-user’s behalf (license information not displayed on boot).

.. note:: By default without any installation information specified, the internet settings is set to ``basic``; kernel parameters ``rhgb`` and ``quiet`` are set and display licenses is set to ``true``.

If you are using YAML:

.. code-block:: yaml

	---
	installation:
	  timezone: Europe/London
	  internetSettings: basic
	  kernelParams:
	  - rhgb
	  - quiet
	  diskSize: 12288
	  swapSize: 512
	  displayLicenses: false

If you are using JSON:

.. code-block:: json

	{
	  "installation": {
	    "timezone": "Europe/London",
	    "internetSettings": "basic",
	    "kernelParams": [
	      "rhgb",
	      "quiet"
	    ],
	    "diskSize": 12288,
	    "swapSize": 512,
	    "displayLicenses": false
	  }
	}