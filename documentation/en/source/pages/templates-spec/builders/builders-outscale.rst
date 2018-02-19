.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-outscale:

Outscale
========

Default builder type: ``Outscale``

Require Cloud Account: Yes

`outscale.com <http://outscale.com>`_

The Outscale builder provides information for building and publishing the machine image for Outscale cloud platform. The Outscale builder requires cloud account information to upload and register the machine image to Outscale cloud.
This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The Outscale builder section has the following definition when using YAML:

.. code-block:: yaml

    ---
    builders:
    - type: Outscale
        # the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

    {
      "builders": [
        {
          "type": "Outscale",
          ...the rest of the definition goes here.
        }
      ]
    }

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Outscale: ``Outscale``. To get the available builder type, please refer to :ref:`command-line-format`
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
    * ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. If the machine image is to be stored in Amazon S3, the maximum disk size is 10GB, otherwise if this is an EBS-backed machine image the maximum disk size is 1TB.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Outscale: ``Outscale``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing the Cloudstack cloud account information required to publish the built machine image.
* ``region`` (mandatory): a string providing the region where to publish the machine image. See below for valid regions.

Valid Regions
-------------

The following regions are supported:

* ``eu-west-2``: EU (France) Region
* ``us-east-2``: US East (New Jersey) Region
* ``us-west-1``: US West (California) Region
* ``cn-southeast-1``: Asia Pacific (Hong-Kong) Region

Outscale Cloud Account
----------------------

Key: ``account``
Used to authenticate to Outscale cloud platform.

The Outscale cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for Outscale: ``Outscale``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a ``builder`` section to reference the rest of the cloud account information.
* ``secretAccessKey`` (mandatory): A string providing your Outscale secret access key
* ``accessKey`` (mandatory): A string providing your Outscale access key id

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows an Outscale builder with all the information to build and publish a machine image to Outscale.

If you are using YAML:

.. code-block:: yaml

    ---
    builders:
    - type: Outscale
      account:
        type: Outscale
        name: My Outscale Account
        accessKey: 789456123ajdiewjd
        secretAccessKey: ks30hPeH1xWqilJ04
      installation:
        diskSize: 10240
      region: eu-west-2
      description: centos-template

If you are using JSON:

.. code-block:: json

    {
      "builders": [
        {
          "type": "Outscale",
          "account": {
            "type": "Outscale",
            "name": "My Outscale Account",
            "accessKey": "789456123ajdiewjd",
            "secretAccessKey": "ks30hPeH1xWqilJ04"
          },
          "installation": {
            "diskSize": 10240
          },
          "region": "eu-west-2",
          "description": "centos-template"
        }
      ]
    }

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``outscale-account.yml``.

.. code-block:: yaml

    ---
    accounts:
    - type: Outscale
      name: My Outscale Account
      accessKey: 789456123ajdiewjd
      secretAccessKey: ks30hPeH1xWqilJ04

If you are using JSON, create a JSON file ``outscale-account.json``:

.. code-block:: json

    {
      "accounts": [
        {
          "type": "Outscale",
          "name": "My Outscale Account",
          "accessKey": "789456123ajdiewjd",
          "secretAccessKey": "ks30hPeH1xWqilJ04"
        }
      ]
    }

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

If you are using YAML:

.. code-block:: yaml

    ---
    builders:
    - type: Outscale
      account:
        file: "/home/joris/accounts/outscale-account.yml"
      installation:
        diskSize: 10240
      region: eu-west-2

If you are using JSON:

.. code-block:: json

    {
      "builders": [
        {
          "type": "Outscale",
          "account": {
            "file": "/home/joris/accounts/outscale-account.json"
          },
          "installation": {
            "diskSize": 10240
          },
          "region": "eu-west-2",
        }
      ]
    }

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

    ---
    builders:
    - type: Outscale
      account:
        name: My Outscale Account
      installation:
        diskSize: 10240
      region: eu-west-2

If you are using JSON:

.. code-block:: json

    {
      "builders": [
        {
          "type": "Outscale",
          "account": {
            "name": "My Outscale Account"
          },
          "installation": {
            "diskSize": 10240
          },
          "region": "eu-west-2",
        }
      ]
    }
