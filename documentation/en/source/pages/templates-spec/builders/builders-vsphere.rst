.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-vmware-vsphere:

VMware vSphere vCenter
======================

Builder type: ``VMware vCenter``

Require Cloud Account: Yes

The VMware vCenter builder provides information for building VMware vSphere vCenter compatible machine images.
This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The VMware vCenter builder section has the following definition when using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: VMware vCenter
  # the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "VMware vCenter",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for VMware vCenter: ``VMware vCenter``. To get the available builder type, please refer to :ref:`command-line-format`
* ``hardwareSettings`` (mandatory): an object providing hardware settings to be used for the machine image. The following valid keys for hardware settings are:
	* ``memory`` (mandatory): an integer providing the amount of RAM to provide to an instance provisioned from the machine image (in MB).
	* ``hwType`` (optional): an integer providing the hardware type for the machine image. This is the VMware hardware type: 4 (ESXi>3.x), 7 (ESXi>4.x) or 9 (ESXi>5.x)
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for VMware vCenter: ``VMware vCenter``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing the VMware vSphere vCenter cloud account information required to publish the built machine image.
* ``displayName`` (mandatory): a string providing the name of the machine image to display in VMware vSphere vCenter.
* ``esxHost`` (mandatory): a string providing the esxHost name or ip address.
* ``datastore`` (mandatory): a string providing the name of the datastore where to store the machine image.
* ``network`` (optional): a string providing the virtual network name.

vSphere vCenter Cloud Account
-----------------------------

Key: ``account``
Used to authenticate to VMware vSphere vCenter.

The vCenter cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for VMware vCenter: ``VMware vCenter``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``login`` (mandatory): a string providing the user name to use to authenticate to the VMware vSphere vCenter platform
* ``password`` (mandatory): a string providing the password to use to authenticate to the VMware vSphere vCenter platform
* ``hostname`` (mandatory): a string providing the fully-qualified hostname or IP address of the VMware vSphere vCenter platform.
* ``proxyHostname`` (optional): a string providing the fully qualified hostname or IP address of the proxy to reach the VMware vSphere vCenter platform.
* ``port`` (optional): an integer providing the VMware vSphere vCenter platform port number (by default: 443 is used).
* ``proxyPort`` (optional): an integer providing the proxy port number to use to reach the VMware vSphere vCenter platform.

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows an vCenter builder with all the information to build and publish a machine image to VMware vSphere vCenter.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: VMware vCenter
    account:
      type: VMware vCenter
      name: My VCenter account
      login: mylogin
      password: mypassword
      hostname: myhostname
      proxyHostname: myproxyHostname
      proxyPort: '6354'
      port: '443'
    hardwareSettings:
      memory: 1024
      hwType: 7
    installation:
      diskSize: 10240
    esxHost: my_esx_host
    datastore: my_datastore
    displayName: test_Hammr
    network: VM_Network

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "VMware vCenter",
        "account": {
          "type": "VMware vCenter",
          "name": "My VCenter account",
          "login": "mylogin",
          "password": "mypassword",
          "hostname": "myhostname",
          "proxyHostname": "myproxyHostname",
          "proxyPort": "6354",
          "port": "443"
        },
        "hardwareSettings": {
          "memory": 1024,
          "hwType": 7
        },
        "installation": {
          "diskSize": 10240
        },
        "esxHost": "my_esx_host",
        "datastore": "my_datastore",
        "displayName": "test_Hammr",
        "network": "VM_Network"
      }
    ]
  }

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``vcenter-account.yml``.

.. code-block:: yaml

  ---
  accounts:
  - type: VMware vCenter
    name: My VCenter account
    login: mylogin
    password: mypassword
    hostname: myhostname
    proxyHostname: myproxyHostname
    proxyPort: '6354'
    port: '443'

If you are using JSON, create a JSON file ``vcenter-account.json``:

.. code-block:: json

  {
    "accounts": [
      {
        "type": "VMware vCenter",
        "name": "My VCenter account",
        "login": "mylogin",
        "password": "mypassword",
        "hostname": "myhostname",
        "proxyHostname": "myproxyHostname",
        "proxyPort": "6354",
        "port": "443"
      }
    ]
  }

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: VMware vCenter
    account:
      file: "/home/joris/accounts/vcenter-account.yml"
    hardwareSettings:
      memory: 1024
      hwType: 7
    installation:
      diskSize: 10240
    esxHost: my_esx_host
    datastore: my_datastore
    displayName: test_Hammr
    network: VM_Network

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "VMware vCenter",
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
        "esxHost": "my_esx_host",
        "datastore": "my_datastore",
        "displayName": "test_Hammr",
        "network": "VM_Network"
      }
    ]
  }

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: VMware vCenter
    account:
      name: My vCenter Account
    hardwareSettings:
      memory: 1024
      hwType: 7
    installation:
      diskSize: 10240
    esxHost: my_esx_host
    datastore: my_datastore
    displayName: test_Hammr
    network: VM_Network

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "VMware vCenter",
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
        "esxHost": "my_esx_host",
        "datastore": "my_datastore",
        "displayName": "test_Hammr",
        "network": "VM_Network"
      }
    ]
  }