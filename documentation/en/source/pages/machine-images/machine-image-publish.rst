.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _machine-image-publish:

Publishing a Machine Image
==========================

In order to publish a machine image of the template you created, you must make sure that the ``builders`` section of the template has the necessary info for each machine image you want to publish. This includes defining the machine image you want to build as well the information for the cloud platform you want to publish to.

You will also need to set the information for your cloud account. We recommend that this information not be included in the template file, but rather set as a value that hammr will access in a seperate read-only file. For more information on creating a credential file with your cloud account information refer to the details in :ref:`cloud-accounts`.

The following is a YAML example of the builders section illustrating the publication to OpenStack. Note that you can incorporate details for several cloud platforms in the same configuration file. For details of the required parameters for each of the image types, refer to the documentation. You can use either YAML or JSON to create your template.

.. code-block:: yaml

	---
	builders:
	- type: openstack
	  hardwareSettings:
	    memory: 1024
	  installation:
	    diskSize: 2000
	  account: Openstack OW2
	  tenant: opencloudware
	  imageName: openstack-test
	  publicImage: 'no'
	  endpoint: http://ow2-04.xsalto.net:9292/v1
	  keystoneEndpoint: http://ow2-04.xsalto.net:5000/v2.0
	  username: test
	  password: password

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "openstack",
	      "hardwareSettings": {
	        "memory": 1024
	      },
	      "installation": {
	        "diskSize": 2000
	      },
	      "account": "Openstack OW2",
	      "tenant": "opencloudware",
	      "imageName": "openstack-test",
	      "publicImage": "no",
	      "endpoint": "http://ow2-04.xsalto.net:9292/v1",
	      "keystoneEndpoint": "http://ow2-04.xsalto.net:5000/v2.0",
	      "username": "test",
	      "password": "password"
	    }
	  ]
	}

Publish the image(s) by running the command ``image publish``:

.. code-block:: shell

	$ hammr image publish --id <the id> --file <your-template>.yml
	Validating the template file [/tmp/centOS.yml] ...
	OK: Syntax of template file [/tmp/centOS.yml] is ok
	Publishing 'ami' image (1/1)
	|>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>| 100%: Done, published o... |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<|
	OK: Publication to 'amazon' is ok
	Cloud ID : ami-25aa6752

.. note:: This may take some time. A progress report is shown.

To get the id of the machine image generated, use the command ``image list``:

.. code-block:: shell

	$ hammr image list
	Getting all images and publications for [root] ...
	Images:
	+------+---------------+---------+------+-----------+---------------------+------+------------+-------------------+
	|  Id  |     Name      | Version | Rev. |  Format   |       Created       | Size | Compressed | Generation Status |
	+======+===============+=========+======+===========+=====================+======+============+===================+
	| 1042 | generation    | 1.0     | 1    | kvm       | 2014-05-21 09:29:36 | 0B   | X          | Done              |
	+------+---------------+---------+------+-----------+---------------------+------+------------+-------------------+
	| 1049 | generation    | 1.0     | 1    | ovf       | 2014-05-21 12:17:21 | 0B   | X          | In progress (2%)  |
	+------+---------------+---------+------+-----------+---------------------+------+------------+-------------------+
	| 981  | wordpress     | 1.0     | 1    | vbox      | 2014-05-19 17:08:06 | 0B   | X          | Canceled          |
	+------+---------------+---------+------+-----------+---------------------+------+------------+-------------------+
	| 960  | nginx-muppets | 1.0     | 1    | vbox      | 2014-05-15 13:33:43 | 0B   | X          | Done              |
	+------+---------------+---------+------+-----------+---------------------+------+------------+-------------------+

	Found 4 images
	No publication available

