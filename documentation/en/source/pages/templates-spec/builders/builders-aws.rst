.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _builder-aws:

Amazon EC2
==========

Builder type: ``ami``

Require Cloud Account: Yes
`aws.amazon.com <aws.amazon.com>`_

The Amazon builder provides information for building and publishing machine images for Amazon EC2. The Amazon builder requires cloud account information to upload and register the machine image to AWS (Amazon Web Services) public cloud.

The Amazon builder section has the following definition:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "ami",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``account`` (mandatory): an object providing the AWS cloud account information required to publish the built machine image.
* ``disableRootLogin`` (optional): a boolean flag to determine if root login access should be disabled for any instance provisioned from the machine image.
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. If the machine image is to be stored in Amazon S3, the maximum disk size is 10GB, otherwise if this is an EBS-backed machine image the maximum disk size is 1TB.
* ``ebs`` (optional): a boolean flag to determine if the machine image should be EBS-backed.
* ``type`` (mandatory): the builder type, ``ami``

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``account`` (mandatory): an object providing the AWS cloud account information required to publish the built machine image.
* ``region`` (mandatory): a string providing the region where to publish the machine image. See below for valid regions.
* ``s3bucket`` (mandatory): a string providing the bucket name where to store the machine image. Bucket names are global to everyone, so you must choose a unique bucket name that does not already exist (or belongs to you). A bucket name cannot include spaces. Note, that if the bucket exists already in one region (for example Europe) and you wish to upload the same machine image to another region, then you must provide a new bucket name.
* ``type`` (mandatory): the builder type, ``ami``

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

Amazon Cloud Account
--------------------

Key: ``account``

Used to authenticate to AWS.

The Amazon cloud account has the following valid keys:

* ``accessKey`` (mandatory): A string providing your AWS access key id. To get your access key, sign into AWS (aws.amazon.com), click on Security Credentials > Access Credentials > Access Keys. Your access key id should be displayed, otherwise create a new one. Note, for security purposes, we recommend you change your access keys every 90 days
* ``accountNumber`` (mandatory): A string providing your AWS account number. This number can be found at the top right hand side of the Account > Security Credentials page after signing into amazon web services
* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.
* ``keyPairPrivateKey`` (optional): A string providing the pathname or URL where to retrieve the private key of a key pair that has been created in AWS. This is mandatory if you wish to create an EBS-backed (elastic block storage) machine image. The private key is used to create an instance of the image in AWS in order to attach an EBS volume and create the EBS-backed machine image. To create a key pair, sign into amazon web services (aws.amazon.com), click on Key Pairs to create a new key pair. Download and save the private key. This should be a (.pem) file.
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``secretAccessKey`` (mandatory): A string providing you AWS secret access key. To get your secret access key, sign into AWS (aws.amazon.com), click on Security Credentials > Access Credentials > Access Keys. Click on the Show button to reveal your secret key
* ``type`` (mandatory): a string providing the cloud account type: aws.
* ``x509Cert`` (mandatory): A string providing the pathname or URL where to retrieve the X.509 certificate public key. To create a X.509 certificate, sign into AWS (aws.amazon.com), click on Security Credentials > Access Credentials > X.509 Certificates. Download the X.509 certificate or create a new one. This should be a (.pem) file.
* ``x509PrivateKey`` (mandatory): A string providing the pathname or URL where to retrieve the X.509 certificate private key. This private key is provided during the X.509 creation process. AWS does not store this private key, so you must download it and store it during this creation process. To create a X.509 certificate, sign into AWS (aws.amazon.com), click on Security Credentials > Access Credentials > X.509 Certificates and create a new certificate. Download and save the Private Key. This should be a (.pem) file

Note: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows an amazon builder with all the information to build and publish a machine image to Amazon EC2.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "ami",
	      "account": {
	        "type": "ami",
	        "name": "My AWS Account",
	        "accountNumber": "111122223333",
	        "x509PrivateKey": "/home/joris/accounts/aws/pk509.pem",
	        "x509Cert": "/home/joris/accounts/aws/cert509.pem",
	        "accessKey": "789456123ajdiewjd",
	        "secretAccessKey": "ks30hPeH1xWqilJ04",
	        "keyPairPrivateKey": "/home/joris/accounts/aws/pk-mykeypair.pem"
	      },
	      "installation": {
	        "diskSize": 10240
	      },
	      "region": "eu-west-1",
	      "s3bucket": "joris-uss-bucket"
	    }
	  ]
	}

Referencing the Cloud Account

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a json file ``aws-account.json``.

.. code-block:: json

	{
	  "accounts": [
	    {
	      "type": "ami",
	      "name": "My AWS Account",
	      "accountNumber": "111122223333",
	      "x509PrivateKey": "/home/joris/accounts/aws/pk509.pem",
	      "x509Cert": "/home/joris/accounts/aws/cert509.pem",
	      "accessKey": "789456123ajdiewjd",
	      "secretAccessKey": "ks30hPeH1xWqilJ04",
	      "keyPairPrivateKey": "/home/joris/accounts/aws/pk-mykeypair.pem"
	    }
	  ]
	}

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "ami",
	      "account": {
	        "file": "/home/joris/accounts/aws-account.json"
	      },
	      "installation": {
	        "diskSize": 10240
	      },
	      "region": "eu-west-1",
	      "s3bucket": "joris-uss-bucket"
	    }
	  ]
	}

Reference by name, note the cloud account must already be created by using ``account create``.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "ami",
	      "account": {
	        "name": "My AWS Account"
	      },
	      "installation": {
	        "diskSize": 10240
	      },
	      "region": "eu-west-1",
	      "s3bucket": "joris-uss-bucket"
	    }
	  ]
	}