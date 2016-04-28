.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _builder-flexiant:

Flexiant
========

Builder type: ``flexiant-kvm``, ``flexiant-ova`` or ``flexiant-raw``

Require Cloud Account: Yes
`flexiant.com <http://flexiant.com>`_

The Flexiant builder provides information for building and publishing the machine image to a Flexiant cloud platform. This builder supports KVM (``flexiant-kvm``), VMware (``flexiant-ova``) or Raw (``flexiant-raw``) based images for Flexiant.

The Flexiant builder requires cloud account information to upload and register the machine image to the Flexiant platform.

The Flexiant builder section has the following definition:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "flexiant-ova",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``hardwareSettings`` (mandatory): an object providing hardware settings to be used for the machine image. If an OVF machine image is being built, then the hardware settings are mandatory. The following valid keys for hardware settings are:
	* ``memory`` (mandatory): an integer providing the amount of RAM to provide to an instance provisioned from the machine image (in MB).
* installation (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.
* ``type`` (optional): a string providing the machine image type to build. For Flexiant: ``flexiant-kvm``, ``flexiant-ovf`` or ``flexiant-raw``.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``account`` (mandatory): an object providing the Flexiant cloud account information required to publish the built machine image.
* ``virtualDatacenter`` (mandatory): a string providing the datacenter name where to register the machine image. Note, the user must have access to this datacenter.
* ``imageName`` (mandatory): a string providing the name of the machine image to displayed.
* ``diskOffering`` (mandatory): a string providing the disk offering to register the machine image under.
* ``type`` (mandatory): a string providing the machine image type to build. For Flexiant: ``flexiant-kvm``, ``flexiant-ovf`` or ``flexiant-raw``.

Flexiant Cloud Account
----------------------

Key: ``account``
Used to authenticate the Flexiant platform.

The Flexiant cloud account has the following valid keys:

* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``password`` (mandatory): a string providing your flexiant cloud orchestrator account password
* ``username`` (mandatory): a string providing your API username. To get your api username, log in to flexiant cloud orchestrator, click on Settings > Your API Details
* ``wsdlURL`` (mandatory): a string providing the wsdl URL of the flexiant cloud orchestrator, for example: https://myapi.example2.com:4442/?wsdl

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows a Flexiant builder with all the information to build and publish a machine image to the Flexiant.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "flexiant-ova",
	      "account": {
	        "type": "flexiant",
	        "name": "My Flexiant Account",
	        "username": "test.test@test.fr/hsefjuhseufhew",
	        "password": "myPassWD",
	        "wsdlURL": "https://20.20.20.20:4442/?wsdl"
	      },
	      "hardwareSettings": {
	        "memory": 1024
	      },
	      "installation": {
	        "diskSize": 2000
	      },
	      "imageName": "CentOS Core",
	      "virtualDatacenter": "vdc1",
	      "diskOffering": "50 GB"
	    }
	  ]
	}

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a json file ``flexiant-account.json``.

.. code-block:: json

	{
	  "accounts": [
	    {
	      "type": "flexiant",
	      "name": "My Flexiant Account",
	      "username": "test.test@test.fr/hsefjuhseufhew",
	      "password": "myPassWD",
	      "wsdlURL": "https://20.20.20.20:4442/?wsdl"
	    }
	  ]
	}

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "flexiant-ova",
	      "account": {
	        "file": "/home/joris/accounts/flexiant-account.json"
	      },
	      "hardwareSettings": {
	        "memory": 1024
	      },
	      "installation": {
	        "diskSize": 2000
	      },
	      "imageName": "CentOS Core",
	      "virtualDatacenter": "c8c1873f-799c-3453-b46c-f5db63116b05",
	      "diskOffering": "61afdd81-43d9-39b5-9150-cffe9071b1b9"
	    }
	  ]
	}

Reference by name, note the cloud account must already be created by using ``account create``.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "flexiant-ova",
	      "account": {
	        "name": "My Flexiant Account"
	      },
	      "hardwareSettings": {
	        "memory": 1024
	      },
	      "installation": {
	        "diskSize": 2000
	      },
	      "imageName": "CentOS Core",
	      "datacenterUUID": "vdc1",
	      "diskOffering": "50 GB"
	    }
	  ]
	}
