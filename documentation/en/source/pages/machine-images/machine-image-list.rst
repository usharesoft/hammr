.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _machine-image-list:

Listing the Images Generated
============================

You can check that the machine images have been created by running ``image list``:

.. code-block:: shell

	$ hammr image list
	Getting all images and publications for [root] ...
	Images:
	+------+---------------+---------+------+-----------+---------------------+------+------------+-------------------+
	|  Id  |     Name      | Version | Rev. |  Format   |       Created       | Size | Compressed | Generation Status |
	+======+===============+=========+======+===========+=====================+======+============+===================+
	| 1042 | generation    | 1.0     | 1    | kvm       | 2014-05-21 09:29:36 | 0B   | X          | Done              |
	+------+---------------+---------+------+-----------+---------------------+------+------------+-------------------+
	| 981  | wordpress     | 1.0     | 1    | vbox      | 2014-05-19 17:08:06 | 0B   | X          | Canceled          |
	+------+---------------+---------+------+-----------+---------------------+------+------------+-------------------+
	| 960  | nginx-muppets | 1.0     | 1    | vbox      | 2014-05-15 13:33:43 | 0B   | X          | Done              |
	+------+---------------+---------+------+-----------+---------------------+------+------------+-------------------+

	Found 3 images
	No publication available

The table lists the image ID number, which you will need to publish the image, the name, version, revision (this is automatically increased everytime you modify the template and run ``template build``), the format of the image, when it was created (date and time of the creation), if the image is compressed (not possible for all formats) and the status.
