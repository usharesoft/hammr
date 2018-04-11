.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-installation-partitioning-lv:

logical volumes
===============

Within a :ref:`stack-installation-partitioning` section, the ``logicalVolumes`` sub-section describes the way a volume group should be partitioned.

The definition of a ``logicalVolumes`` section when using YAML is:

.. code-block:: yaml

	---
	disks:
	- # the list of logical volumes goes here.

If you are using JSON:

.. code-block:: javascript

	"disks": [
	    ...the list of logical volumes goes here.
	]

The valid keys to use within a logical volume are:

* ``fstype`` (mandatory): a string providing the filesystem type. See below for valid values.
* ``grow`` (optional): a boolean marking this volume (partition) as growable. When a volume is growable it will take any available space remaining in the volume group after all the other volumes catered for. You can only have 1 growable partition in the logical volume.
* ``label`` (optional): a string providing a label for this volume
* ``mountPoint`` (mandatory): a string providing the mount point of the volume.
* ``name`` (mandatory): a string providing the name of the volume.
* ``size`` (mandatory): an integer providing the size of the volume. Note that the sum of all the volumes cannot be greater than the total size provided in the :ref:`stack-installation-partitioning-vg`.
* ``vg_name`` (mandatory): a string providing the name of the volume group this logical volume is using

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
