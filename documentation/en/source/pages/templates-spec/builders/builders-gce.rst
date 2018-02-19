.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-gce:

Google Compute Engine
=====================

Default builder type: ``Google Compute Engine``

Require Cloud Account: Yes

`Google Compute Engine <https://cloud.google.com/compute/>`_

The GCE builder provides information for building and publishing the machine image for Googe Compute Engine. The GCE builder requires cloud account information to upload and register the machine image to Google Compute Engine public cloud.
This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The GCE builder section has the following definition when using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Google Compute Engine
		# the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "Google Compute Engine",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Google compute Engine: ``Google Compute Engine``. To get the available builder type, please refer to :ref:`command-line-format`
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:


* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Google compute Engine: ``Google Compute Engine``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing the GCE cloud account information required to publish the built machine image.
* ``bucket`` (mandatory): a string providing the bucket name where to store the machine image. The bucket name can only contain lower case alpha characters [a-z] and the special character “-”.
* ``bucketLocation`` (mandatory): a string providing the bucket location where to store the machine image. See below for valid values.
* ``computeZone`` (mandatory): a string providing the compute zone where this machine image will be used. See below for valid compute zone values.
* ``description`` (optional): a string providing the description for the machine image.
* ``diskNamePrefix`` (mandatory): a string providing the disk name prefix used when creating the disks for the running machine (note the prefix name can only contain lower case alpha characters [a-z] and the special character ”-”)
* ``projectId`` (mandatory): a string providing the project Id to associate this machine image with.
* ``storageClass`` (mandatory): a string providing the storage type to use with this machine image. See below for valid storage class values


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

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for Google Compute Engine: ``Google Compute Engine``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``certPassword`` (mandatory): A string providing the password to decrypt the GCE certificate. This password is normally provided along with the certificate.
* ``cert`` (mandatory): A string providing the pathname or URL where to retrieve your GCE certificate. This should be a (.pem) file.
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.


.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows a GCE builder with all the information to build and publish a machine image to Google Compute Engine.

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Google Compute Engine
	  account:
	    type: Google Compute Engine
	    name: My GCE Account
	    username: joris
	    certPassword: myCertPassword
	    cert: "/home/joris/certs/gce.pem"
	  computeZone: europe-west1-a
	  bucketLocation: EU
	  bucket: jorisbucketname
	  projectId: jorisproject
	  storageClass: STANDARD
	  diskNamePrefix: uss-
	  description: CentOS Core machine image

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Google Compute Engine",
	      "account": {
	        "type": "Google Compute Engine",
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

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``gce-account.yml``.

.. code-block:: yaml

	---
	accounts:
	- type: Google Compute Engine
	  name: My GCE Account
	  username: joris
	  certPassword: myCertPassword
	  cert: "/home/joris/certs/gce.pem"

If you are using JSON, create a JSON file ``gce-account.json``:

.. code-block:: json

	{
	  "accounts": [
	    {
	        "type": "Google Compute Engine",
	        "name": "My GCE Account",
	        "username": "joris",
	        "certPassword": "myCertPassword",
	        "cert": "/home/joris/certs/gce.pem"
	    }
	  ]
	}

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Google Compute Engine
	  account:
	    file: "/home/joris/accounts/gce-account.yml"
	  computeZone: europe-west1-a
	  bucketLocation: EU
	  bucket: jorisbucketname
	  projectId: jorisproject
	  storageClass: STANDARD
	  diskNamePrefix: uss-
	  description: CentOS Core machine image

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Google Compute Engine",
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

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Google Compute Engine
	  account:
	    name: My GCE Account
	  computeZone: europe-west1-a
	  bucketLocation: EU
	  bucket: jorisbucketname
	  projectId: jorisproject
	  storageClass: STANDARD
	  diskNamePrefix: uss-
	  description: CentOS Core machine image

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Google Compute Engine",
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
