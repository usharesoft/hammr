.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _adv-partitioning-disks:

Disks
=====

The first thing a partitioning table needs is to declare one or more disks that will be used to partition. Each disk declared in the partitioning table has the name ``sd`` followed by a letter, starting at ``a``, namely: 1st disk ``sda``, 2nd disk ``sdb`` and so on. A disk is one of two types, either ``MSDOS`` or ``LVM``, and provides a total disk size available. LVM disks cannot have any physical partitions, however can be used in logical volumes (refer to :ref:`adv-partitioning-logical-grp-vol`).

The example below describes 1 disk of 20GB when using YAML.

.. code-block:: yaml

	---
	installation:
	  partitioning:
		disks:
		- name: sda
		  type: msdos
		  size: 20480

If you are using JSON:

.. code-block:: json

	{
	  "installation": {
	    "partitioning": {
	      "disks": [
	        {
	          "name": "sda",
	          "type": "msdos",
	          "size": 20480
	        }
	      ]
	    }
	  }
	}

Example
-------

The following example describes 2 disks of 20GB each when using YAML.

.. code-block:: yaml

	---
	installation:
	  partitioning:
		disks:
		- name: sda
		  type: msdos
		  size: 20480
		- name: sdb
		  type: msdos
		  size: 20480

If you are using JSON:

.. code-block:: json

	{
	  "installation": {
	    "partitioning": {
	      "disks": [
	        {
	          "name": "sda",
	          "type": "msdos",
	          "size": 20480
	        },
	        {
	          "name": "sdb",
	          "type": "msdos",
	          "size": 20480
	        }
	      ]
	    }
	  }
	}
