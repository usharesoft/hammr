.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _machine-image-deploy:

Deploying a Published Machine Image
===================================

In order to deploy a machine image already published, you must make sure that the builders section of the template has the necessary info. For information on publishing a machine image, refer to :ref:`machine-image-publish`.

The following is a YAML example of the builders section illustrating the deployment of a published image to OpenStack. For details of the required parameters for each of the published image formats, refer to the documentation. You can use either YAML or JSON to create your template.

.. code-block:: yaml

        ---
        provisioner:
          type: OpenStack
          name: MyDeploy
          region: GRA1
          network: Ext-Net
          flavor: vps-ssd-2

If you are using JSON:

.. code-block:: json

  {
    "provisioner": {
      "type": "OpenStack",
      "name": "MyDeploy",
      "region": "GRA1",
      "network": "Ext-Net",
      "flavor": "vps-ssd-2"
    }
  }


You can deploy an instance of a published machine image by running ``image deploy``:

.. code-block:: shell

	$ hammr image deploy --publish-id <the id> --file <your file>
        Deployment in progress
        |##################################################################################################################|
        OK: Deployment is successful
        Deployment id: [ayhis3j148]
        Region: eu-west-1
        IP address: 54.171.53.9

To get the id of the machine image published, use the command ``image list``. Any images published will appear in the second table ``Publications``, where the ``Publish ID`` is listed.

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
