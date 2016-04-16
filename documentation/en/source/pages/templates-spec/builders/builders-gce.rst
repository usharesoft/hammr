.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _builder-gce:

Google Compute Engine
=====================

Builder type: ``gce``

Require Cloud Account: Yes
`Google Compute Engine <https://cloud.google.com/compute/>`_

The GCE builder provides information for building and publishing the machine image for Googe Compute Engine. The GCE builder requires cloud account information to upload and register the machine image to Google Compute Engine public cloud.

The GCE builder section has the following definition:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "gce",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``account`` (mandatory): an object providing the GCE cloud account information required to publish the built machine image.
* ``bucket`` (mandatory): a string providing the bucket name where to store the machine image. The bucket name can only contain lower case alpha characters [a-z] and the special character “-”.
* ``bucketLocation`` (mandatory): a string providing the bucket location where to store the machine image. See below for valid values.
* ``computeZone`` (mandatory): a string providing the compute zone where this machine image will be used. See below for valid compute zone values.
* ``description`` (optional): a string providing the description for the machine image.
* ``diskNamePrefix`` (mandatory): a string providing the disk name prefix used when creating the disks for the running machine (note the prefix name can only contain lower case alpha characters [a-z] and the special character ”-”)
* ``projectId`` (mandatory): a string providing the project Id to associate this machine image with.
* ``storageClass`` (mandatory): a string providing the storage type to use with this machine image. See below for valid storage class values
* ``type`` (mandatory): the builder type: ``gce``

Valid Compute Zones
-------------------

The following zones are supported:

* ``us-central1-a``: US (availability zone: a)
* ``us-central1-b``: US (availability zone: b)
* ``europe-west1-a``: Europe (availability zone: a)
* ``europe-west1-a``: Europe (availability zone: b)

Valid Bucket Locations
----------------------

The following bucket locations are supported:

* ``EU``
* ``US``

Valid Storage Classes
---------------------

The following storage classes are supported:

* ``STANDARD``
* ``DURABLE_REDUCED_AVAILABILITY``

GCE Cloud Account
-----------------

Key: ``account``
Used to authenticate to GCE.

The GCE cloud account has the following valid keys:

* ``certPassword`` (mandatory): A string providing the password to decrypt the GCE certificate. This password is normally provided along with the certificate.
* ``cert`` (mandatory): A string providing the pathname or URL where to retrieve your GCE certificate. This should be a (.pem) file.
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``type`` (mandatory): a string providing the cloud account type: ``gce``.

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows a GCE builder with all the information to build and publish a machine image to Google Compute Engine.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "gce",
	      "account": {
	        "type": "gce",
	        "name": "My GCE Account",
	        "username": "joris",
	        "certPassword": "myCertPassword",
	        "cert": "/home/joris/certs/gce.pem"
	      },
	      "computeZone": "europe-west1-a",
	      "bucketLocation": "EU",
	      "bucket": "jorisbucketname",
	      "projectId": "jorisproject",
	      "storageClass": "STANDARD",
	      "diskNamePrefix": "uss-",
	      "description": "CentOS Core machine image"
	    }
	  ]
	}

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a json file ``gce-account.json``.

.. code-block:: json

	{
	  "accounts": [
	    {
	        "type": "gce",
	        "name": "My GCE Account",
	        "username": "joris",
	        "certPassword": "myCertPassword",
	        "cert": "/home/joris/certs/gce.pem"
	    }
	  ]
	}

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "gce",
	      "account": {
	        "file": "/home/joris/accounts/gce-account.json"
	      },
	      "computeZone": "europe-west1-a",
	      "bucketLocation": "EU",
	      "bucket": "jorisbucketname",
	      "projectId": "jorisproject",
	      "storageClass": "STANDARD",
	      "diskNamePrefix": "uss-",
	      "description": "CentOS Core machine image"
	    }
	  ]
	}

Reference by name, note the cloud account must already be created by using ``account create``.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "gce",
	      "account": {
	        "name": "My GCE Account"
	      },
	      "computeZone": "europe-west1-a",
	      "bucketLocation": "EU",
	      "bucket": "jorisbucketname",
	      "projectId": "jorisproject",
	      "storageClass": "STANDARD",
	      "diskNamePrefix": "uss-",
	      "description": "CentOS Core machine image"
	    }
	  ]
	}
