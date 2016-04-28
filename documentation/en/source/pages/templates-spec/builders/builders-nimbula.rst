.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _builder-nimbula:

Nimbula
=======

Builder type: ``nimbula-esx`` or ``nimbula-kvm``
Require Cloud Account: Yes

The Nimbula builder provides information for building and publishing the machine image to the Nimbula cloud platform. This builder supports KVM (``nimbula-kvm``) or VMware (``nimbula-esx``) based images for Nimbula.

The Nimbula builder requires cloud account information to upload and register the machine image to the Nimbula platform.
The Nimbula builder section has the following definition:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "nimbula-kvm",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``hardwareSettings`` (mandatory): an object providing hardware settings to be used for the machine image. If an OVF machine image is being built, then the hardware settings are mandatory. The following valid keys for hardware settings are:
	* ``memory`` (mandatory): an integer providing the amount of RAM to provide to an instance provisioned from the machine image (in MB).
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.
* ``type`` (optional): a string providing the machine image type to build. For Nimbula: ``nimbula-kvm`` or ``nimbula-esx``.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``account`` (mandatory): an object providing the Nimbula cloud account information required to publish the built machine image.
* ``description`` (mandatory): a string providing the description that will be displayed for the machine image.
* ``imageListName`` (mandatory): a string providing the list name where to register the machine image. Note that this is the full pathname, for example ``/usharesoft/administrator/myimages``. Machine images can be added to an image list to create a versioned selection of related machine images recording the versions of the image over its lifetime. An image maintainer can add newer versions of a machine image to the image list and can set the default version to be used when this image list is invoked in a launch plan to deploy VM instances
* ``imageVersion`` (mandatory): a string providing the version of the machine image being registered.
* ``type`` (optional): a string providing the machine image type to build. For Nimbula: ``nimbula-kvm`` or ``nimbula-esx``.

Nimbula Cloud Account
---------------------

Key: ``account``

Used to authenticate the Nimbula platform.
The Nimbula cloud account has the following valid keys:

* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.
* ``endpoint`` (mandatory): URL endpoint of the Nimbula cloud
* name (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``password`` (mandatory): a string providing the password used to to authenticate to Nimbula Director
* ``username`` (mandatory): a string providing the user used to authenticate to Nimbula Director. This is in the form of a URI, for example ``/root/root``
* ``type`` (mandatory): a string providing the cloud account type: ``nimbula``.

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows an Nimbula builder with all the information to build and publish a machine image to Nimbula.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "nimbula-kvm",
	      "account": {
	        "type": "nimbula",
	        "name": "My Nimbula Account",
	        "endpoint": "http://20.20.20.201",
	        "username": "myLogin",
	        "password": "myPassWD"
	      },
	      "hardwareSettings": {
	        "memory": 1024
	      },
	      "installation": {
	        "diskSize": 2000
	      },
	      "imageListName": "/usharesoft/administrator/myimages",
	      "imageVersion": "1",
	      "description": "CentOS Core Image"
	    }
	  ]
	}

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a json file ``nimbula-account.json``.

.. code-block:: json

	{
	  "accounts": [
	    {
	        "type": "nimbula",
	        "name": "My Nimbula Account",
	        "endpoint": "http://20.20.20.201",
	        "username": "myLogin",
	        "password": "myPassWD"
	    }
	  ]
	}

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "nimbula-kvm",
	      "account": {
	        "file": "/home/joris/accounts/nimbula-account.json"
	      },
	      "hardwareSettings": {
	        "memory": 1024
	      },
	      "installation": {
	        "diskSize": 2000
	      },
	      "imageListName": "/usharesoft/administrator/myimages",
	      "imageVersion": "1",
	      "description": "CentOS Core Image"
	    }
	  ]
	}

Reference by name, note the cloud account must already be created by using ``account create``.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "nimbula-kvm",
	      "account": {
	        "name": "My Nimbula Account"
	      },
	      "hardwareSettings": {
	        "memory": 1024
	      },
	      "installation": {
	        "diskSize": 2000
	      },
	      "imageListName": "/usharesoft/administrator/myimages",
	      "imageVersion": "1",
	      "description": "CentOS Core Image"
	    }
	  ]
	}
