.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _machine-image-deploy:

Deploying a published machine image
===================================

You can deploy an instance of a published machine image by running ``image deploy``:

.. code-block:: shell

	$ hammr image deploy --publish-id <the publish id> --name <your-deployment-name>
        Deployment in progress
        |##################################################################################################################|
        OK: Deployment is successful
        Deployment id: [ayhis3j148]
        Region: eu-west-1
        IP address: 54.171.53.9

To get the id of the machine image generated, use the command ``image list``:

.. code-block:: shell

	$ hammr image list
        Getting all images and publications for [root] ...
        Images:
	+------+---------------+---------+------+-----------+---------------------+------+------------+-------------------+
	|  Id  |     Name      | Version | Rev. |  Format   |       Created       | Size | Compressed | Generation Status |
	+======+===============+=========+======+===========+=====================+======+============+===================+
	| 1042 | generation    | 1.0     | 1    | Amazon    | 2014-05-21 09:29:36 | 325M | X          | Done              |
	+------+---------------+---------+------+-----------+---------------------+------+------------+-------------------+
	| 981  | wordpress     | 1.0     | 1    | vbox      | 2014-05-19 17:08:06 | 0B   | X          | Canceled          |
	+------+---------------+---------+------+-----------+---------------------+------+------------+-------------------+
	| 960  | nginx-muppets | 1.0     | 1    | vbox      | 2014-05-15 13:33:43 | 0B   | X          | Done              |
        +------+---------------+---------+------+-----------+---------------------+------+------------+-------------------+

        Found 5 images
        Publications:
        +-----------------------+----------+------------+---------------+-----------+--------------+-------------------+
        |       Template name   | Image ID | Publish ID | Account name  |  Format   | Cloud ID     |      Status       |
        +=======================+==========+============+===============+===========+==============+===================+
        | my-appliance          | 12       | 111        | USS AWS       | Amazon    | ami-87f216fe | Done              |
        +-----------------------+----------+------------+---------------+-----------+--------------+-------------------+

        Found 1 publication
