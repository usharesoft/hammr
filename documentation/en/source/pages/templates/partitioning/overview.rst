.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _adv-partitioning:

Using Advanced Partitioning
===========================

Hammr supports the ability to describe partitioning schemas as part of the stack used to build machine images. Partitioning is the act of dividing one or more physical disks into logical sections with the goal to treat each physical disk drive as if it were multiple disks.

Partitioning is used frequently in production systems. Benefits include:

* Isolating data from programs
* Keeping frequently used programs and data near each other
* Having cache and log files separate from other files. These can change size dynamically and rapidly, potentially making a file system full.
* Having a separate area for operating system virtual memory swapping/paging

.. warning:: Some cloud platforms do not support all the features of partitioning, or limit the number of partitions you may have in your machine image. When building a machine image for a particular cloud platform, hammr will return an error if the partitioning setup is not supported. This helps you save time and effort down the road when an instance of the machine image does not boot.

The rest of this section provides examples of:

.. toctree::
   :titlesonly:

   adv-partitioning-disks
   adv-partitioning-partitions
   adv-partitioning-logical-partitions
   adv-partitioning-grow-partitions
   adv-partitioning-logical-grp-vol
   
   
   



