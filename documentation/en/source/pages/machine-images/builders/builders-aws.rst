.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-aws:

Amazon EC2
==========

Default builder type: ``Amazon AWS``

Require Cloud Account: Yes

`aws.amazon.com <aws.amazon.com>`_

The Amazon builder provides information for building and publishing machine images for Amazon EC2. The Amazon builder requires cloud account information to upload and register the machine image to AWS (Amazon Web Services) public cloud.
This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The Amazon builder section has the following definition when using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Amazon AWS
    # the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "Amazon AWS",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Amazon: ``Amazon AWS``. To get the available builder type, please refer to :ref:`command-line-format`
* ``disableRootLogin`` (optional): a boolean flag to determine if root login access should be disabled for any instance provisioned from the machine image.
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. As EBS-backed machine image is created, the maximum disk size is 1TB.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Amazon: ``Amazon AWS``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing the AWS cloud account information required to publish the built machine image.
* ``region`` (mandatory): a string providing the region where to publish the machine image. See :ref:`amazon-regions` for valid regions.
* ``bucket`` (mandatory): a string providing the bucket name where to store the machine image. Bucket names are global to everyone, so you must choose a unique bucket name that does not already exist (or belongs to you). A bucket name cannot include spaces. Note, that if the bucket exists already in one region (for example Europe) and you wish to upload the same machine image to another region, then you must provide a new bucket name.

.. _amazon-regions:

Valid Regions
-------------

The following regions are supported:

* ``ap-northeast-1``: Asia Pacific (Tokyo) Region
* ``ap-southeast-1``: Asia Pacific (Singapore) Region
* ``eu-west-1``: EU (Ireland) Region
* ``sa-east-1``: South America (Sao Paulo) Region
* ``us-east-1``: US East (North Virginia) Region
* ``us-west-1``: US West (North california) Region
* ``us-west-2``: US West (Oregon) Region

Deploying a Published Machine Image
-----------------------------------

To deploy a published machine image to Amazon the builder section must have the following definition when using YAML:

.. code-block:: yaml

  ---
  provisioner:
    type: Amazon
    name: MyDeploy
    cores: 1
    memory: 1024

If you are using JSON:

.. code-block:: javascript

  {
    "provisioner": {
      "type": "Amazon",
      "name": "MyDeploy",
      "cores": 1,
      "memory": 1024
    }
  }

The valid keys are:

* ``type`` (mandatory): a string providing the cloud provider on which the published image should be deployed.
* ``name`` (mandatory): the name of the published machine image
* ``cores`` (optional): if not specified default values will be used 
* ``memory`` (optional): if not specified default values will be used 


Amazon Cloud Account
--------------------

Key: ``account``

Used to authenticate to AWS.

The Amazon cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for Amazon: ``Amazon``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``accountNumber`` (mandatory): A string providing your AWS account number. This number can be found at the top right hand side of the Account > Security Credentials page after signing into Amazon Web Services
* ``accessKeyId`` (mandatory): A string providing your AWS access key id. To get your access key, sign into AWS (aws.amazon.com), click on Security Credentials > Access Credentials > Access Keys. Your access key id should be displayed, otherwise create a new one. Note, for security purposes, we recommend you change your access keys every 90 days
* ``secretAccessKeyId`` (mandatory): A string providing you AWS secret access key. To get your secret access key, sign into AWS (aws.amazon.com), click on Security Credentials > Access Credentials > Access Keys. Click on the Show button to reveal your secret key
* ``x509Cert`` (mandatory): A string providing the pathname or URL where to retrieve the X.509 certificate public key. To create a X.509 certificate, sign into AWS (aws.amazon.com), click on Security Credentials > Access Credentials > X.509 Certificates. Download the X.509 certificate or create a new one. This should be a (.pem) file.
* ``x509PrivateKey`` (mandatory): A string providing the pathname or URL where to retrieve the X.509 certificate private key. This private key is provided during the X.509 creation process. AWS does not store this private key, so you must download it and store it during this creation process. To create a X.509 certificate, sign into AWS (aws.amazon.com), click on Security Credentials > Access Credentials > X.509 Certificates and create a new certificate. Download and save the Private Key. This should be a (.pem) file
* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows an amazon builder with all the information to build and publish a machine image to Amazon EC2.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Amazon AWS
    account:
      type: Amazon
      name: My AWS account
      accountNumber: 11111-111111-1111
      accessKeyId: myaccessKeyid
      secretAccessKeyId: mysecretaccesskeyid
      x509Cert: "/path/to/aws.cert.pem"
      x509PrivateKey: "/path/to/aws.key.pem"
    installation:
      diskSize: 10240
    region: eu-central-1
    bucket: testsohammr

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Amazon AWS",
        "account": {
          "type": "Amazon",
          "name": "My AWS account",
          "accountNumber": "11111-111111-1111",
          "accessKeyId": "myaccessKeyid",
          "secretAccessKeyId": "mysecretaccesskeyid",
          "x509Cert": "/path/to/aws.cert.pem",
          "x509PrivateKey": "/path/to/aws.key.pem"
        },
        "installation": {
          "diskSize": 10240
        },
        "region": "eu-central-1",
        "bucket": "testsohammr"
      }
    ]
  }

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``aws-account.yml``.

.. code-block:: yaml

  ---
  accounts:
  - type: Amazon
    accountNumber: 11111-111111-1111
    name: My AWS account
    accessKeyId: myaccessKeyid
    secretAccessKeyId: mysecretaccesskeyid
    x509Cert: "/path/to/aws.cert.pem"
    x509PrivateKey: "/path/to/aws.key.pem"

If you are using JSON, create a JSON file ``aws-account.json``:

.. code-block:: json

  {
    "accounts": [
      {
        "type": "Amazon",
        "accountNumber": "11111-111111-1111",
        "name": "My AWS account",
        "accessKeyId": "myaccessKeyid",
        "secretAccessKeyId": "mysecretaccesskeyid",
        "x509Cert": "/path/to/aws.cert.pem",
        "x509PrivateKey": "/path/to/aws.key.pem"
      }
    ]
  }

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Amazon AWS
    account:
      file: "/path/to/aws-account.yml"
    installation:
      diskSize: 10240
    region: eu-central-1
    bucket: test-so-hammr

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Amazon AWS",
        "account": {
              "file": "/path/to/aws-account.json"
        },
        "installation": {
          "diskSize": 10240
        },
        "region": "eu-central-1",
        "bucket": "test-so-hammr"
      }
    ]
  }

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Amazon AWS
    account:
      name: My AWS Account
    installation:
      diskSize: 10240
    region: eu-central-1
    bucket: test-so-hammr

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Amazon AWS",
        "account": {
              "name": "My AWS Account"
        },
        "installation": {
          "diskSize": 10240
        },
        "region": "eu-central-1",
        "bucket": "test-so-hammr"
      }
    ]
  }
