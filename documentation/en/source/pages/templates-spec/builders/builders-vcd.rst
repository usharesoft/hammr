.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-vmware-vcd:

VMware vCloud Director
======================

Default builder type: ``VMware vCloud Director``

Require Cloud Account: Yes

The VMware vCloud Director builder provides information for building VMware vCloud Director compatible machine images.
The VMware VCD builder section has the following definition when using YAML:

.. code-block:: yaml

	---
	builders:
	- type: VMware vCloud Director
		# the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "VMware vCloud Director",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for VMware vCloud Director: ``VMware vCloud Director``. To get the available builder type, please refer to :ref:`command-line-format`
* ``hardwareSettings`` (mandatory): an object providing hardware settings to be used for the machine image. The following valid keys for hardware settings are:
	* ``memory`` (mandatory): an integer providing the amount of RAM to provide to an instance provisioned from the machine image (in MB).
	* ``hwType`` (optional): an integer providing the hardware type for the machine image. This is the VMware hardware type: 4 (ESXi>3.x), 7 (ESXi>4.x) or 9 (ESXi>5.x)
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for VMware vCloud Director: ``VMware vCloud Director``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing the vCloud Director cloud account information required to publish the built machine image.
* ``catalogName`` (mandatory): a string providing the name of the catalog to register the machine image. Catalogs contain references to virtual systems and media images.
* ``imageName`` (mandatory): a string providing the name of the machine image to display in VCD.
* ``orgName`` (mandatory): a string providing the name of the vCloud organization to register the machine image.

vCloud Director Cloud Account
-----------------------------

Key: ``account``
Used to authenticate to VMware vCloud Director.

The VCD cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for VMware vCloud Director: ``VMware vCloud Director``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``hostname`` (mandatory): a string providing the fully-qualified hostname or IP address of the vCloud Directory platform.
* ``password`` (mandatory): a string providing the password to use to authenticate to the vCloud Director platform
* ``port`` (optional): an integer providing the vCloud Director platform port number (by default: 443 is used).
* ``proxyHostname`` (optional): a string providing the fully qualified hostname or IP address of the proxy to reach the vCloud Director platform.
* ``proxyPort`` (optional): an integer providing the proxy port number to use to reach the vCloud Director platform.
* ``username`` (mandatory): a string providing the user name to use to authenticate to the vCloud Director platform

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows a VCD builder with all the information to build and publish a machine image to VMware vCloud Director.

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: VMware vCloud Director
	  account:
	    type: VMware vCloud Director
	    name: My VCD Account
	    hostname: 10.1.1.2
	    username: joris
	    password: mypassword
	  hardwareSettings:
	    memory: 1024
	    hwType: 7
	  installation:
	    diskSize: 10240
	  orgName: HQProd
	  catalogName: myCatalog
	  imageName: CentOS Core

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "VMware vCloud Director",
	      "account": {
	        "type": "VMware vCloud Director",
	        "name": "My VCD Account",
	        "hostname": "10.1.1.2",
	        "username": "joris",
	        "password": "mypassword"
	      },
	      "hardwareSettings": {
	        "memory": 1024,
	        "hwType": 7
	      },
	      "installation": {
	        "diskSize": 10240
	      },
	      "orgName": "HQProd",
	      "catalogName": "myCatalog",
	      "imageName": "CentOS Core"
	    }
	  ]
	}

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a yaml file ``vcd-account.yml``.

.. code-block:: yaml

	---
	accounts:
	- type: VMware vCloud Director
	  name: My VCD Account
	  hostname: 10.1.1.2
	  username: joris
	  password: mypassword


If you are using JSON, create a JSON file ``vcd-account.json``:

.. code-block:: json

	{
	  "accounts": [
	    {
	      "type": "VMware vCloud Director",
	      "name": "My VCD Account",
	      "hostname": "10.1.1.2",
	      "username": "joris",
	      "password": "mypassword"
	    }
	  ]
	}

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: VMware vCloud Director
	  account:
	    file: "/home/joris/accounts/vcd-account.yml"
	  hardwareSettings:
	    memory: 1024
	    hwType: 7
	  installation:
	    diskSize: 10240
	  orgName: HQProd
	  catalogName: myCatalog
	  imageName: CentOS Core

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "VMware vCloud Director",
	      "account": {
	        "file": "/home/joris/accounts/vcd-account.json"
	      },
	      "hardwareSettings": {
	        "memory": 1024,
	        "hwType": 7
	      },
	      "installation": {
	        "diskSize": 10240
	      },
	      "orgName": "HQProd",
	      "catalogName": "myCatalog",
	      "imageName": "CentOS Core"
	    }
	  ]
	}

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: VMware vCloud Director
	  account:
	    name: My VCD Account
	  hardwareSettings:
	    memory: 1024
	    hwType: 7
	  installation:
	    diskSize: 10240
	  orgName: HQProd
	  catalogName: myCatalog
	  imageName: CentOS Core

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "VMware vCloud Director",
	      "account": {
	        "name": "My VCD Account"
	      },
	      "hardwareSettings": {
	        "memory": 1024,
	        "hwType": 7
	      },
	      "installation": {
	        "diskSize": 10240
	      },
	      "orgName": "HQProd",
	      "catalogName": "myCatalog",
	      "imageName": "CentOS Core"
	    }
	  ]
	}
