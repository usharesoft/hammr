.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _your-quota:

Quotas
======

There are a number of quotas that can be set on a UForge account. For example, a free account has the following limitations:

Quotas can be set for the following:

* Disk usage: diskusage in bytes (includes storage of bundle uploads, bootscripts, image generations, scans)
* Templates: number of templates created
* Generations: number of machine images generated
* Scans: number of scans for migration

To view the quotas that have been set on your account, run ``quota list``:

.. code-block:: shell

	$ hammr quota list
	Getting quotas for [root] ...
	Scans (25)                --------------------UNLIMITED---------------------
	Templates (26)            --------------------UNLIMITED---------------------
	Generations (72/100)      ||||||||||||||||||||||||||||||||||||--------------
	Disk usage (30GB)         --------------------UNLIMITED---------------------

The output not only lists any quotas that are set, but it also shows you the limit you are at, even if your account is set to unlimited.