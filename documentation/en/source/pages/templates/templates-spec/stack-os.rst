.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-os:

os
==

Within a ``stack``, the ``os`` sub-section describes the operating system to use when building the machine image. This includes the operating system version, architecture and the os profile to use. The os profile is a pre-determined group of packages that will be installed as part of the machine image build. Extra packages can be specified to include in the build that are available in the operating system repository, and the build date can be set to get the latest updates, or roll-back. For more information on os package updates, refer to :ref:`pkg-updating`.

To use a particular operating system, you must have access to it in the UForge server you are using. To determine which operating systems are available, use the ``os list`` command (please refer :ref:`command-line` for more information).

The definition of an ``os`` section when using YAML is:

.. code-block:: yaml

	---
	os:
	  # the os definition goes here

If you are using JSON:

.. code-block:: javascript

	"os": {
	    ...the os definition goes here.
	}

The valid keys to use within the os object are:

* ``arch`` (mandatory): a string providing the architecture to use
* ``name`` (mandatory): a string providing the name of the operating system to use
* ``pkgs`` (optional): an array providing any extra packages to install (see pkgs key sub-section for more information)
* ``profile`` (mandatory): a string providing which operating system profile to use
* ``updateTo`` (optional): a string providing the date and time where package versions should be calculated (determines which package versions to use to * calculate the package dependency tree)
* ``version`` (mandatory): a string providing the version of the operating system to use

Sub-Sections
------------

The ``os`` sub-sections are:

.. toctree::
   :titlesonly:

   stack-os-pkgs


Examples
--------

Basic Example
~~~~~~~~~~~~~

The following example describes using CentOS 6.4 64 bit operating system for the template. The profile ``Minimal`` is used, which automatically adds a pre-determined group of packages to the template.

If you are using YAML:

.. code-block:: yaml

	---
	os:
	  name: CentOS
	  version: '6.4'
	  arch: x86_64
	  profile: Minimal

If you are using JSON:

.. code-block:: json

	{
	  "os": {
	    "name": "CentOS",
	    "version": "6.4",
	    "arch": "x86_64",
	    "profile": "Minimal"
	  }
	}

The name, version, arch and profile values for an operating system can be found by using the command ``os list``. This lists all the operating systems you have access to.

Specifying a Build Date/Time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By using the ``updateTo`` key will specify the date and time to calculate the version and release of all the packages to use in the template during the build phase of a machine image. This allows you to roll-back or update the operating system packages used. If no date is provided, then the date the template is created is used. The example below sets the date to 14 May 2014 00:00 UTC. Note that timezone must respect `General Time Zone <http://docs.oracle.com/javase/7/docs/api/java/text/SimpleDateFormat.html#timezone>`_ format.

If you are using YAML:

.. code-block:: yaml

	---
	os:
	  name: CentOS
	  version: '6.4'
	  arch: x86_64
	  profile: Minimal
	  updateTo: 2014-05-14 00:00 UTC

If you are using JSON:

.. code-block:: json

	{
	  "os": {
	    "name": "CentOS",
	    "version": "6.4",
	    "arch": "x86_64",
	    "profile": "Minimal"
	    "updateTo": "2014-05-14 00:00 UTC"
	  }
	}

You can still use a date without time information, in such case time will be interpreted by server as midnight in server's own timezone (UTC by default). 

If you are using YAML:

.. code-block:: yaml

	---
	os:
	  name: CentOS
	  version: '6.4'
	  arch: x86_64
	  profile: Minimal
	  updateTo: '2014-05-14'

If you are using JSON:

.. code-block:: json

	{
	  "os": {
	    "name": "CentOS",
	    "version": "6.4",
	    "arch": "x86_64",
	    "profile": "Minimal"
	    "updateTo": "2014-05-14"
	  }
	}
