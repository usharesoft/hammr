.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-nimbula:

Nimbula
=======

Default builder type: ``Nimbula ESX`` or ``Nimbula KVM``

Require Cloud Account: Yes

The Nimbula builder provides information for building and publishing the machine image to the Nimbula cloud platform. This builder supports KVM (``Nimbula KVM``) or VMware (``Nimbula ESX``) based images for Nimbula.
These builder types are the default names provided by UForge AppCenter.

.. note:: These builder type names can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The Nimbula builder requires cloud account information to upload and register the machine image to the Nimbula platform.
The Nimbula builder section has the following definition when using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Nimbula KVM
		# the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "Nimbula KVM",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Nimbula: ``Nimbula ESX` or, ``Nimbula KVMK``. To get the available builder type, please refer to :ref:`command-line-format`
* ``hardwareSettings`` (mandatory): an object providing hardware settings to be used for the machine image. If an OVF machine image is being built, then the hardware settings are mandatory. The following valid keys for hardware settings are:
	* ``memory`` (mandatory): an integer providing the amount of RAM to provide to an instance provisioned from the machine image (in MB).
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Nimbula: ``Nimbula ESX` or, ``Nimbula KVMK``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing the Nimbula cloud account information required to publish the built machine image.
* ``description`` (mandatory): a string providing the description that will be displayed for the machine image.
* ``imageListName`` (mandatory): a string providing the list name where to register the machine image. Note that this is the full pathname, for example ``/usharesoft/administrator/myimages``. Machine images can be added to an image list to create a versioned selection of related machine images recording the versions of the image over its lifetime. An image maintainer can add newer versions of a machine image to the image list and can set the default version to be used when this image list is invoked in a launch plan to deploy VM instances
* ``imageVersion`` (mandatory): a string providing the version of the machine image being registered.

Nimbula Cloud Account
---------------------

Key: ``account``

Used to authenticate the Nimbula platform.
The Nimbula cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for Nimbula is ``Nimbula``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.
* ``endpoint`` (mandatory): URL endpoint of the Nimbula cloud
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``password`` (mandatory): a string providing the password used to to authenticate to Nimbula Director
* ``username`` (mandatory): a string providing the user used to authenticate to Nimbula Director. This is in the form of a URI, for example ``/root/root``

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows an Nimbula builder with all the information to build and publish a machine image to Nimbula.

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Nimbula KVM
	  account:
	    type: Nimbula
	    name: My Nimbula Account
	    endpoint: http://20.20.20.201
	    username: myLogin
	    password: myPassWD
	  hardwareSettings:
	    memory: 1024
	  installation:
	    diskSize: 2000
	  imageListName: "/usharesoft/administrator/myimages"
	  imageVersion: '1'
	  description: CentOS Core Image

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Nimbula KVM",
	      "account": {
	        "type": "Nimbula",
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

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``nimbula-account.yml``.

.. code-block:: yaml

	---
	accounts:
	- type: Nimbula
	  name: My Nimbula Account
	  endpoint: http://20.20.20.201
	  username: myLogin
	  password: myPassWD


If you are using JSON, create a JSON file ``nimbula-account.json``:

.. code-block:: json

	{
	  "accounts": [
	    {
	        "type": "Nimbula",
	        "name": "My Nimbula Account",
	        "endpoint": "http://20.20.20.201",
	        "username": "myLogin",
	        "password": "myPassWD"
	    }
	  ]
	}

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Nimbula KVM
	  account:
	    file: "/home/joris/accounts/nimbula-account.yml"
	  hardwareSettings:
	    memory: 1024
	  installation:
	    diskSize: 2000
	  imageListName: "/usharesoft/administrator/myimages"
	  imageVersion: '1'
	  description: CentOS Core Image

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Nimbula KVM",
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

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Nimbula KVM
	  account:
	    name: My Nimbula Account
	  hardwareSettings:
	    memory: 1024
	  installation:
	    diskSize: 2000
	  imageListName: "/usharesoft/administrator/myimages"
	  imageVersion: '1'
	  description: CentOS Core Image

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Nimbula KVM",
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
