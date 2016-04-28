.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _builder-vmware-vsphere:

VMware vSphere vCenter
======================

Builder type: ``vcenter``
Require Cloud Account: Yes

The VMware vCenter builder provides information for building VMware vSphere vCenter compatible machine images.
The VMware vCenter builder section has the following definition:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "vcenter",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``hardwareSettings`` (mandatory): an object providing hardware settings to be used for the machine image. The following valid keys for hardware settings are:
	* ``memory`` (mandatory): an integer providing the amount of RAM to provide to an instance provisioned from the machine image (in MB).
	* ``hwType`` (optional): an integer providing the hardware type for the machine image. This is the VMware hardware type: 4 (ESXi>3.x), 7 (ESXi>4.x) or 9 (ESXi>5.x)
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.
* ``type`` (mandatory): the builder type: ``vcenter``

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``account`` (mandatory): an object providing the VMware vSphere vCenter cloud account information required to publish the built machine image.
* ``cluster`` (mandatory): a string providing the name of the cluster to register the machine image.
* ``datacenterName`` (mandatory): a string providing the name of the datacenter to register the machine image.
* ``datastore`` (mandatory): a string providing the name of the datastore where to store the machine image.
* ``imageName`` (mandatory): a string providing the name of the machine image to display in VMware vSphere vCenter.
* ``type`` (mandatory): a string providing the builder type: ``vcenter``

vSphere vCenter Cloud Account
-----------------------------

Key: ``account``
Used to authenticate to VMware vSphere vCenter.

The vCenter cloud account has the following valid keys:

* ``hostname`` (mandatory): a string providing the fully-qualified hostname or IP address of the VMware vSphere vCenter platform.
* ``password`` (mandatory): a string providing the password to use to authenticate to the VMware vSphere vCenter platform
* ``port`` (optional): an integer providing the VMware vSphere vCenter platform port number (by default: 443 is used).
* ``proxyHostname`` (optional): a string providing the fully qualified hostname or IP address of the proxy to reach the VMware vSphere vCenter platform.
* ``proxyPort`` (optional): an integer providing the proxy port number to use to reach the VMware vSphere vCenter platform.
* ``type`` (mandatory): a string providing the builder type: ``vcenter``
* ``username`` (mandatory): a string providing the user name to use to authenticate to the VMware vSphere vCenter platform

..note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows an vCenter builder with all the information to build and publish a machine image to VMware vSphere vCenter.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "vcenter",
	      "account": {
	        "type": "vcenter",
	        "name": "My vCenter Account",
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
	      "datacenter": "HQProd",
	      "cluster": "myCluster",
	      "datastore": "myDatastore",
	      "imageName": "CentOS Core"
	    }
	  ]
	}

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a json file ``vcenter-account.json``.

.. code-block:: json

	{
	  "accounts": [
	    {
	      "type": "vcenter",
	      "name": "My vCenter Account",
	      "hostname": "10.1.1.2",
	      "username": "joris",
	      "password": "mypassword"
	    }
	  ]
	}

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "vcenter",
	      "account": {
	        "file": "/home/joris/accounts/vcenter-account.json"
	      },
	      "hardwareSettings": {
	        "memory": 1024,
	        "hwType": 7
	      },
	      "installation": {
	        "diskSize": 10240
	      },
	      "datacenter": "HQProd",
	      "cluster": "myCluster",
	      "datastore": "myDatastore",
	      "imageName": "CentOS Core"
	    }
	  ]
	}

Reference by name, note the cloud account must already be created by using ``account create``.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "vcd",
	      "account": {
	        "name": "My vCenter Account"
	      },
	      "hardwareSettings": {
	        "memory": 1024,
	        "hwType": 7
	      },
	      "installation": {
	        "diskSize": 10240
	      },
	      "datacenter": "HQProd",
	      "cluster": "myCluster",
	      "datastore": "myDatastore",
	      "imageName": "CentOS Core"
	    }
	  ]
	}
