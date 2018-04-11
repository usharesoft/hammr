.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-installation-partitioning-vg:

volumeGroups
============

Within a :ref:`stack-installation-partitioning` section, the ``volumeGroups`` sub-section describes a volume group in the partitioning table. A volume group creates a pool of disk space from a collection of disks or partitions. This volume group can then be partitioned via a :ref:`stack-installation-partitioning-lv`. 

.. warning:: Only disks and partitions of type ``lvm`` and logical partitions can be added to a volume group.

The definition of a ``volumeGroups`` section when using YAML is:

.. code-block:: yaml

	---
	disks:
	- # the list of volume groups goes here.

If you are using JSON:

.. code-block:: javascript

	"disks": [
	    ...the list of volume groups goes here.
	]

The valid keys to use within a ``volumeGroup`` are:

* ``name`` (mandatory): a string providing the name of the volume group
* ``physicalVolumes`` (optional): an array of strings describing the names of the disks or partitions to include in this group. The sum of all the disks and partitions added will be the total size of this volume group. This logical pool of disk can then be partitioned via a logical volume. You cannot add a disk and one of its partitions into the same volume group, furthermore you cannot use a disk or partition more than once if 2 or more volume groups are declared.
