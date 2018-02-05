.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-installation-partitioning-disks:

disks
=====

Within a :ref:`stack-installation-partitioning` section, the ``disks`` sub-section describes all the physical disks for an advanced partitioning table. Each disk may be partitioned, i.e. the act of dividing the physical disk into logical sections with the goal to treat one physical disk drive as if it were multiple disks. These are called physical partitions. A disk may have a maximum of 4 physical partitions.

The definition of a ``disks`` section when using YAML is:

.. code-block:: yaml

	---
	disks:
	- # the list of disks goes here.

If you are using JSON:

.. code-block:: javascript

	"disks": [
	    ...the list of disks goes here.
	]

The valid keys to use within a disk are:

* ``name`` (mandatory): a string providing the name of the disk. Currently only the following values are valid: ``sd`` followed by a letter. The first disk must use the letter ``a`` (i.e. ``sda``), the second disk ``b`` and so forth.
* ``partitions`` (optional): an array of objects describing the partitions for this disk. For more information, refer to the :ref:`stack-installation-partitioning-disks-partitions` sub-section. A maximum of 4 partitions is allowed.
* ``size`` (mandatory): an integer providing the size of the disk (in MB)
* ``type`` (mandatory): a string providing the disk type. The valid values are ``MSDOS`` or ``LVM``

Sub-sections
------------

The disks sub-sections are:

.. toctree::
   :titlesonly:

   stack-installation-partitioning-disks-partitions
   