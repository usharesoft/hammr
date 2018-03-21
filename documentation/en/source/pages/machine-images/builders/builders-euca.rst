.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-euca:

Eucalyptus
==========

Default builder type: ``Eucalyptus KVM`` or ``Eucalyptus XEN``

Require Cloud Account: Yes

`www.eucalyptus.com <http://www.eucalyptus.com>`_

The Eucalyptus builder provides information for building and publishing the machine image for Eucalyptus. This builder supports KVM (``Eucalyptus KVM``) and Xen (``Eucalyptus XEN``) based images for Eucalyptus.
These builder types are the default names provided by UForge AppCenter.

.. note:: These builder type names can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The Eucalyptus builder requires cloud account information to upload and register the machine image to an Eucalyptus cloud platform.

The Eucalyptus builder section has the following definition when using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Eucalyptus KVM
		# the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "Eucalyptus KVM",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Eucalyptus: ``Eucalyptus KVM`` or ``Eucalyptus XEN``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing the Eucalyptus cloud account information required to publish the built machine image.
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.
* ``disableRootLogin`` (optional): a boolean flag to determine if root login access should be disabled for any instance provisioned from the machine image.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Eucalyptus: ``Eucalyptus KVM`` or ``Eucalyptus XEN``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing the Eucalyptus cloud account information required to publish the built machine image.
* ``bucket`` (mandatory): a string providing the bucket where to store the machine image. Note, bucket names are global to everyone, so you must choose a unique bucket name that is not used by another user. The bucket name should not include spaces.
* ``description`` (mandatory): a string providing a description of what the machine image does. The description of the machine image is displayed in the console. The description can only be up to 255 characters long. Descriptions longer than 255 characters will be truncated.
* ``imageName`` (mandatory): a string providing the displayed name for the machine image.
* ``kernelId`` (optional): a string providing the kernel Id when booting an instance from the machine image. Note that the kernel id must be already present on the cloud environment. If a kernel Id is not specified, then the default kernel Id registered on the cloud platform will be used.
* ``ramdisk`` (optional): a string providing the ramdisk Id when booting an instance from the machine image. Note that the ramdisk Id must be already present on the cloud environment. If a ramdisk Id is not specified, then the default ramdisk Id registered on the cloud platform will be used.

Eucalyptus Cloud Account
------------------------

Key: ``account``
Used to authenticate to Eucalyptus.

The Eucalyptus cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for Eucalyptus is ``Eucalyptus``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``accountNumber`` (mandatory): a string providing the User ID or Eucalyptus account number of the user who is bundling the image. This value can be found in the eucarc file.
* ``cloudCert`` (mandatory): a string providing the location of the cloud certificate. This may be a path or URL. To get the cloud certificate, login into your Eucalyptus admin console (for example https://myserver.domain.com:8443). Go to the Credentials ZIP-file and click on the button Download credentials. Unzip this file, you should find the certificate with the name cloud-cert.pem
* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.
* ``endpoint`` (mandatory): a string providing the URL of the Eucalyptus Walrus server. To get the walrus server information, login into your Eucalyptus admin console and click on the Configuration tab
* ``name``: (mandatory) a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``queryId`` (mandatory): a string providing your Eucalyptus query id. To get this key, login into your Eucalyptus admin console (for example https://myserver.domain.com:8443). Go to Query Interface Credentials > Show keys, the query id will be displayed.
* ``secretKey`` (mandatory): a string of your your Eucalyptus secret key. To get this key, login into your Eucalyptus admin console (for example https://myserver.domain.com:8443). Go to Query Interface Credentials > Show keys, the secret key will be displayed
* ``x509PrivateKey`` (mandatory): a string providing the location of the X.509 certificate private key. This may be a path or URL. This is the private key of the X.509 certificate. To get an X.509 private key, login into your Eucalyptus admin console, go to Credentials ZIP-file and click on the button Download credentials. Unzip this file, you should find the private key with the name XXXX-XXXX-XXXX-pk.pem.
* ``x509Cert`` (mandatory): a string providing the location of the X.509 certificate public key. This may be a path or URL. To get a X.509 certificate, login into your Eucalyptus admin console, go to the Credentials ZIP-file and click on the button Download credentials. Unzip this file, you should find the certificate with the name XXXX-XXXX-XXXX-cert.pem

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows an Eucalyptus builder with all the information to build and publish a machine image to Eucalyptus.

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Eucalyptus KVM
	  account:
	    type: Eucalyptus
	    name: My Eucalyptus Account
	    accountNumber: '111122223333'
	    x509PrivateKey: "/home/joris/accounts/euca/euca-pk.pem"
	    x509Cert: "/home/joris/accounts/euca/euca-cert.pem"
	    cloudCert: "/home/joris/accounts/euca/cloud-cert.pem"
	    endpoint: http://127.0.0.1/8773
	    queryId: WkVpyXXZ77rXcdeSbds3lkXcr5Jc4GeUtkA
	    secretKey: ir9CKRvOXXTHJXXj8VPRXX7PgxxY9DY0VLng
	  imageName: CentOS Core
	  description: CentOS Base Image
	  bucket: ussprodbucket

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Eucalyptus KVM",
	      "account": {
	        "type": "Eucalyptus",
	        "name": "My Eucalyptus Account",
	        "accountNumber": "111122223333",
	        "x509PrivateKey": "/home/joris/accounts/euca/euca-pk.pem",
	        "x509Cert": "/home/joris/accounts/euca/euca-cert.pem",
	        "cloudCert": "/home/joris/accounts/euca/cloud-cert.pem",
	        "endpoint": "http://127.0.0.1/8773",
	        "queryId": "WkVpyXXZ77rXcdeSbds3lkXcr5Jc4GeUtkA",
	        "secretKey": "ir9CKRvOXXTHJXXj8VPRXX7PgxxY9DY0VLng"
	      },
	      "imageName": "CentOS Core",
	      "description": "CentOS Base Image",
	      "bucket": "ussprodbucket"
	    }
	  ]
	}

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``euca-account.yml``.

.. code-block:: yaml

	---
	accounts:
	- type: Eucalyptus
	  name: My Eucalyptus Account
	  accountNumber: '111122223333'
	  x509PrivateKey: "/home/joris/accounts/euca/euca-pk.pem"
	  x509Cert: "/home/joris/accounts/euca/euca-cert.pem"
	  cloudCert: "/home/joris/accounts/euca/cloud-cert.pem"
	  endpoint: http://127.0.0.1/8773
	  queryId: WkVpyXXZ77rXcdeSbds3lkXcr5Jc4GeUtkA
	  secretKey: ir9CKRvOXXTHJXXj8VPRXX7PgxxY9DY0VLng

If you are using JSON, create a JSON file ``euca-account.json``:

.. code-block:: json

	{
	  "accounts": [
	    {
	      "type": "Eucalyptus",
	      "name": "My Eucalyptus Account",
	      "accountNumber": "111122223333",
	      "x509PrivateKey": "/home/joris/accounts/euca/euca-pk.pem",
	      "x509Cert": "/home/joris/accounts/euca/euca-cert.pem",
	      "cloudCert": "/home/joris/accounts/euca/cloud-cert.pem",
	      "endpoint": "http://127.0.0.1/8773",
	      "queryId": "WkVpyXXZ77rXcdeSbds3lkXcr5Jc4GeUtkA",
	      "secretKey": "ir9CKRvOXXTHJXXj8VPRXX7PgxxY9DY0VLng"
	    }
	  ]
	}

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Eucalyptus KVM
	  account:
	    file: "/home/joris/accounts/euca-account.yml"
	  imageName: CentOS Core
	  description: CentOS Base Image
	  bucket: ussprodbucket

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Eucalyptus KVM",
	      "account": {
	        "file": "/home/joris/accounts/euca-account.json"
	      },
	      "imageName": "CentOS Core",
	      "description": "CentOS Base Image",
	      "bucket": "ussprodbucket"
	    }
	  ]
	}

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Eucalyptus KVM
	  account:
	    name: My Eucalytpus Account
	  imageName: CentOS Core
	  description: CentOS Base Image
	  bucket: ussprodbucket

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Eucalyptus KVM",
	      "account": {
	        "name": "My Eucalytpus Account"
	      },
	      "imageName": "CentOS Core",
	      "description": "CentOS Base Image",
	      "bucket": "ussprodbucket"
	    }
	  ]
	}