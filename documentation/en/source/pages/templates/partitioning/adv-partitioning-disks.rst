.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _adv-partitioning-disks:

Disks
=====

The first thing a partitioning table needs is to declare one or more disks that will be used to partition. Each disk declared in the partitioning table has the name ``sd`` followed by a letter, starting at ``a``, namely: 1st disk ``sda``, 2nd disk ``sdb`` and so on. A disk may have one of two types, either ``MSDOS`` or ``LVM`` and provide a total disk size available. LVM disks cannot have any physical partitions, however can be used in logical volumes (we will touch on this subject later).

The example below describes 1 disk of 20GB.

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

The following example describes 2 disks of 20GB each.

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
	