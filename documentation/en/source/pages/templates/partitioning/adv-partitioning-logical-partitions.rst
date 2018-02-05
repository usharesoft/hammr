.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _adv-partitioning-logical-partitions:

Logical Partitions
==================

Due to the restriction of only having 4 physical partitions for disk, you can further partition a physical partition using logical partitioning. To partition a physical partition, use the filesystem type ``extended``.

.. note:: You can only use the ``extended`` filesystem ONCE for a disk i.e. you can only partition one physical partition in a disk. When using extended you cannot declare a mount point or label. These will be ignored by hammr.

Like a physical partition, each logical partition has a unique number starting at 5 (5,6,7,8 etc) and declares a filesystem type and size. You cannot further partition a logical partition (extended filesystem type cannot be used). There is no limit to the number of logical partitions you may have, however the sum of the logical partitions cannot exceed the size of the physical partition.

Example
-------

The following example shows 3 physical partitions of a disk, where the last physical partition has 3 logical partitions : ``/space``, ``/home`` and ``/tmp``.

.. image:: /images/partitioning-ex6.png

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
		  fstype: Extended
		  size: 17408
		  partitions:
		  - number: 5
			fstype: ext3
			size: 8192
			mountPoint: "/space"
			label: space
		  - number: 6
			fstype: ext3
			size: 8192
			mountPoint: "/home"
			label: home
		  - number: 7
			fstype: ext3
			size: 1024
			mountPoint: "/tmp"
			label: tmp

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
		            "fstype": "Extended",
		            "size": 17408,
		            "partitions": [
		              {
		                "number": 5,
		                "fstype": "ext3",
		                "size": 8192,
		                "mountPoint": "/space",
		                "label": "space"
		              },
		              {
		                "number": 6,
		                "fstype": "ext3",
		                "size": 8192,
		                "mountPoint": "/home",
		                "label": "home"
		              },
		              {
		                "number": 7,
		                "fstype": "ext3",
		                "size": 1024,
		                "mountPoint": "/tmp",
		                "label": "tmp"
		              }
		            ]
		          }
		        ]
		      }
		    ]
		}
	}

