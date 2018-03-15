.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-flexiant:

Flexiant
========

Default builder type: ``Flexiant QCOW2 - KVM/Xen/VMware``, ``Flexiant OVA - VMware`` or ``Flexiant RAW - KVM/Xen``

Require Cloud Account: Yes

`flexiant.com <http://flexiant.com>`_

The Flexiant builder provides information for building and publishing the machine image to a Flexiant cloud platform. This builder supports KVM (``Flexiant QCOW2 - KVM/Xen/VMware``), VMware (``Flexiant OVA - VMware``) or Raw (``Flexiant RAW - KVM/Xen``) based images for Flexiant.

These builder types are the default names provided by UForge AppCenter.

.. note:: These builder type names can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The Flexiant builder requires cloud account information to upload and register the machine image to the Flexiant platform.

The Flexiant builder section has the following definition when using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Flexiant RAW - KVM/Xen
    # the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "Flexiant OVA - VMware",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Flexiant: ``Flexiant QCOW2 - KVM/Xen/VMware``, ``Flexiant OVA - VMware`` or ``Flexiant RAW - KVM/Xen``. To get the available builder type, please refer to :ref:`command-line-format`
* ``hardwareSettings`` (mandatory): an object providing hardware settings to be used for the machine image. If an OVF machine image is being built, then the hardware settings are mandatory. The following valid keys for hardware settings are:
	* ``memory`` (mandatory): an integer providing the amount of RAM to provide to an instance provisioned from the machine image (in MB).
* installation (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Flexiant: ``Flexiant QCOW2 - KVM/Xen/VMware``, ``Flexiant OVA - VMware`` or ``Flexiant RAW - KVM/Xen``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing the Flexiant cloud account information required to publish the built machine image.
* ``virtualDatacenterName`` (mandatory): a string providing the datacenter name where to register the machine image. Note, the user must have access to this datacenter.
* ``machineImageName`` (mandatory): a string providing the name of the machine image to displayed.
* ``diskOffering`` (mandatory): a string providing the disk offering to register the machine image under.

Flexiant Cloud Account
----------------------

Key: ``account``
Used to authenticate the Flexiant platform.

The Flexiant cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for Flexiant is ``Flexiant``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``apiUsername`` (mandatory): a string providing your API username. To get your api username, log in to Flexiant cloud orchestrator, click on Settings > Your API Details
* ``password`` (mandatory): a string providing your Flexiant cloud orchestrator account password
* ``wsdlUrl`` (mandatory): a string providing the wsdl URL of the Flexiant cloud orchestrator, for example: https://myapi.example2.com:4442/?wsdl
* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows a Flexiant builder with all the information to build and publish a machine image to the Flexiant.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Flexiant RAW - KVM/Xen
    account:
      type: Flexiant
      name: My Flexiant account
      apiUsername: name@domain.com/mykey1111
      password: mypassword
      wsdlUrl: myWsdlurl
    hardwareSettings:
      memory: 1024
    installation:
      diskSize: 2000
    virtualDatacenterName: KVM (CEPH Cluster)
    machineImageName: test_hammr
    diskOffering: 21 GB

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Flexiant RAW - KVM/Xen",
        "account": {
          "type": "Flexiant",
          "name": "My Flexiant account",
          "apiUsername": "name@domain.com/mykey1111",
          "password": "mypassword",
          "wsdlUrl": "myWsdlurl"
        },
        "hardwareSettings": {
          "memory": 1024
        },
        "installation": {
          "diskSize": 2000
        },
        "virtualDatacenterName": "KVM (CEPH Cluster)",
        "machineImageName": "test_hammr",
        "diskOffering": "21 GB"
      }
    ]
  }

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``Flexiant-account.yml``.

.. code-block:: yaml

  ---
  accounts:
  - type: Flexiant
    name: My Flexiant account
    apiUsername: name@domain.com/mykey1111
    password: mypassword
    wsdlUrl: myWsdlurl


If you are using JSON, create a JSON file ``Flexiant-account.json``:

.. code-block:: json

  {
    "accounts": [
      {
        "type": "Flexiant",
        "name": "My Flexiant account",
        "apiUsername": "name@domain.com/mykey1111",
        "password": "mypassword",
        "wsdlUrl": "myWsdlurl"
      }
    ]
  }

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Flexiant RAW - KVM/Xen
    account:
      file: "/path/to/flexiant-account.yml"
    hardwareSettings:
      memory: 1024
    installation:
      diskSize: 2000
    virtualDatacenterName: KVM (CEPH Cluster)
    machineImageName: test_hammr
    diskOffering: 21 GB

If you are using JSON:

.. code-block:: json

    {
      "builders": [
        {
          "type": "Flexiant RAW - KVM/Xen",
          "account": {
            "file": "/path/to/flexiant-account.json"
              },
          "hardwareSettings": {
            "memory": 1024
          },
          "installation": {
            "diskSize": 2000
          },
          "virtualDatacenterName": "KVM (CEPH Cluster)",
          "machineImageName": "test_hammr",
          "diskOffering": "21 GB"
        }
      ]
    }

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Flexiant RAW - KVM/Xen
    account:
      name: My Flexiant Account
    hardwareSettings:
      memory: 1024
    installation:
      diskSize: 2000
    virtualDatacenterName: KVM (CEPH Cluster)
    machineImageName: test_hammr
    diskOffering: 21 GB

If you are using JSON:

.. code-block:: json

    {
      "builders": [
        {
          "type": "Flexiant RAW - KVM/Xen",
          "account": {
            "name": "My Flexiant Account"
              },
          "hardwareSettings": {
            "memory": 1024
          },
          "installation": {
            "diskSize": 2000
          },
          "virtualDatacenterName": "KVM (CEPH Cluster)",
          "machineImageName": "test_hammr",
          "diskOffering": "21 GB"
        }
      ]
    }