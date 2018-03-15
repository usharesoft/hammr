.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _adv-partitioning-logical-grp-vol:

Volume Groups and Logical Volumes
=================================

Volume groups and logical volumes allows more creative and flexible partitioning schemas to be created than conventional partitioning schemas we have already discussed.

A volume group allows you to gather disks, physical and logical partitions into a single logical pool of storage. This pool of storage can then be partitioned (like a disk) by using a logical volume.

Only disks that have the type ``lvm``, and physical partitions or logical partitions that have filesystem types ``lvm2`` can be grouped together in a volume group.

.. note:: Once a physical or logical partition is grouped together into a volume group, they cannot be declared in another volume group.

In this example, an extended physical partition that has two logical partitions that have ``lvm`` filesystems; and a disk of type ``lvm`` are pooled together via a volume group ``grp1``. A logical volume is used to partition further this volume group.

.. image:: /images/partitioning-ex41.png

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
		  mountPoint: "/boot"
		  size: 1024
		- number: 2
		  fstype: linux-swap
		  size: 1024
		- number: 3
		  fstype: extended
		  size: 18432
		  partitions:
		  - number: 5
			fstype: lvm2
			size: 9216
		  - number: 6
			fstype: lvm2
			size: 9216
	  - name: sdb
		type: lvm
		size: 122880
	  volumeGroups:
	  - name: grp1
		physicalVolumes:
		- name: sda5
		- name: sda6
		- name: sdb
	  logicalVolumes:
	  - name: vol1
		vg_name: grp1
		fstype: ext3
		mountPoint: "/home"
		size: 4098
	  - name: vol2
		vg_name: grp1
		fstype: ext3
		mountPoint: "/space"
		size: 64
		grow: true

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
		            "mountPoint": "/boot",
		            "size": 1024
		          },
		          {
		            "number": 2,
		            "fstype": "linux-swap",
		            "size": 1024
		          },
		          {
		            "number": 3,
		            "fstype": "extended",
		            "size": 18432,
		            "partitions": [
		              {
		                "number": 5,
		                "fstype": "lvm2",
		                "size": 9216
		              },
		              {
		                "number": 6,
		                "fstype": "lvm2",
		                "size": 9216
		              }
		            ]
		          }
		        ]
		      },
		      {
		        "name": "sdb",
		        "type": "lvm",
		        "size": 122880
		      }
		    ],
		    "volumeGroups": [
		      {
		        "name": "grp1",
		        "physicalVolumes": [
		          {
		            "name": "sda5"
		          },
		          {
		            "name": "sda6"
		          },
		          {
		            "name": "sdb"
		          }
		        ]
		      }
		    ],
		    "logicalVolumes": [
		      {
		        "name": "vol1",
		        "vg_name": "grp1",
		        "fstype": "ext3",
		        "mountPoint": "/home",
		        "size": 4098
		      },
		      {
		        "name": "vol2",
		        "vg_name": "grp1",
		        "fstype": "ext3",
		        "mountPoint": "/space",
		        "size": 64,
		        "grow": true
		      }
		    ]
	  	}
	}

