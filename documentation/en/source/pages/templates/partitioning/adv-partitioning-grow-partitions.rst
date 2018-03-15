.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _adv-partitioning-grow-partitions:

Growable Partitions
===================

Physical and logical partitions can be marked as growable by using the ``grow`` flag. This declares that the particular partition takes all remaining disk space available after the other partition sizes have been satisfied.

You can only declare one physical partition to be growable in a disk, and one logical partition to be growable for a physical partition.

Example
-------

In this example we mark the “space” physical partition as growable, i.e. the “space” partition takes up the rest of the disk (rather than us having to calculate the space left after creating the first two partitions). We must specify though a size for the “space” partition (the minimum partition size is 64MB).

.. image:: /images/partitioning-ex2.png

.. code-block:: yaml

	---
	partitioning:
	  disks:
	  - name: sda
		type: msdos
		size: 20480
		partitions:
		- number: 1
		  fstype: ext3
		  size: 2048
		  mountPoint: "/boot"
		- number: 2
		  fstype: linux-swap
		  size: 1024
		- number: 3
		  fstype: ext3
		  size: 64
		  grow: true
		  label: space
		  mountPoint: "/space"

If you are using JSON:

.. code-block:: json

	{
		"partitioning": {
		    "disks": [
		      {
		        "name": "sda",
		        "type": "msdos",
		        "size": 20480,
		        "partitions": [
		          {
		            "number": 1,
		            "fstype": "ext3",
		            "size": 2048,
		            "mountPoint": "/boot"
		          },
		          {
		            "number": 2,
		            "fstype": "linux-swap",
		            "size": 1024
		          },
		          {
		            "number": 3,
		            "fstype": "ext3",
		            "size": 64,
		            "grow": true,
		            "label": "space",
		            "mountPoint": "/space"
		          }
		        ]
		      }
		    ]
	    }
	}
