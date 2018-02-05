.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-installation-partitioning-disks-partitions:

partitions
==========

Within a :ref:`stack-installation-partitioning-disks` section, the ``partitions`` sub-section describes all the partitions to create for the disk. Disk partitioning is the act of dividing the physical disk into logical sections with the goal to treat one physical disk drive as if it were multiple disks. 

.. warning:: A disk may have a maximum of 4 partitions.

The definition of a ``partitions`` section when using YAML is:

.. code-block:: yaml

	---
	partitions:
	- # the list of partitions goes here.

If you are using JSON:

.. code-block:: javascript

	"partitions": [
	    ...the list of partitions goes here.
	]

The valid keys to use within a partition are:

* ``fstype`` (mandatory): a string providing the filesystem type. See below for valid values.
* ``grow`` (optional): a boolean marking this partition as growable. When a partition is growable it will take any available space left on the disk after all the other partitions catered for. You can only have 1 growable partition in a disk.
* ``label`` (optional): a string providing a label for this partition
* ``partitions`` (optional): an array of objects ``partition`` describing any logical partitions this partition may contain. To use logical partitions, this partition must use the ``Extended`` filesystem type.
* ``mountPoint`` (optional): a string providing the mount point of the partition. If the ``fstype`` is NOT ``lvm`` then the mount point is mandatory.
* ``number`` (mandatory): an integer providing the partition number. Starting at 1
* ``size`` (mandatory): an integer providing the size of the partition. Note that the sum of all the partitions cannot be greater than the total disk size provided in the ``disk``. The minimum size is 64MB.

Available Filesystem Types
--------------------------

The following are valid filesystem types used with the ``fstype`` key:

* ``Extended``
* ``ext2``
* ``ext3``
* ``ext4``
* ``NTFS``
* ``FAT16``
* ``FAT32``
* ``jfs``
* ``linux-swap``
* ``lvm2``
* ``unformated``
* ``xfs``

