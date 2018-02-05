.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _pkg-updating:

Package Updates
===============

As you probably know, packages evolve as bugs are fixed and new features are added. These new packages become available in the operating system repository. The UForge Server uses an internal mechanism to check for any new package update available in the repository, and, if found, adds the meta-data of this package to its own database. Using this process, the UForge Server builds a history of the operating system, as it keeps references to the old packages that are being replaced by the update.

These updates do not get taken into account for your current template when generating a new image. By calculating packages by the same date ensures when you build your machine image, the same image is generated time after time. This is due to always using the ``updateTo`` date (or the creation date) of the template in question.

Ok great, but what if you actually wanted to include these updates in the next generation? Well, it’s a simple matter of updating the ``updateTo`` key of the stack section.

If you are using YAML:

.. code-block:: yaml

	---
	stack:
	  name: CentOS Base Template
	  version: '6.4'
	  description: This is a CentOS core template.
	  os:
		name: CentOS
		version: '6.4'
		arch: x86_64
		profile: Minimal
		updateTo: '2013-06-15'

If you are using JSON:

.. code-block:: json

	{
		"stack": {
		    "name": "CentOS Base Template",
		    "version": "6.4",
		    "description": "This is a CentOS core template.",
		    "os": {
		      "name": "CentOS",
		      "version": "6.4",
		      "arch": "x86_64",
		      "profile": "Minimal",
		      "updateTo": "2013-06-15"
		    }
		}
	}

.. image:: /images/package-updates2.png

In this case, UForge will notify you that three updates are available. Note, that for package B even if there is an intermediary package (version 7.3), only the last one is taken into account.

