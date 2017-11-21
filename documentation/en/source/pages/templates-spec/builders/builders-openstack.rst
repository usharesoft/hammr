.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _builder-openstack:

OpenStack
=========

Default builder type: ``OpenStack QCOW2``, ``OpenStack VMDK``, ``OpenStack VHD`` or ``OpenStack VDI``

Require Cloud Account: Yes

`www.openstack.org <http://www.openstack.org>`_

The OpenStack builder provides information for building and publishing the machine image to the OpenStack cloud platform. This builder supports KVM (``OpenStack QCOW2``), VMware (``OpenStack VMDK``), Microsoft (``OpenStack VHD``) or VirtualBox (``OpenStack VDI``) based images for Openstack.
These builder types are the default names provided by UForge AppCenter.

.. note:: These builder type names can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The OpenStack builder requires cloud account information to upload and register the machine image to the OpenStack platform.

The OpenStack builder section has the following definition when using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: OpenStack QCOW2
    # the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "OpenStack QCOW2",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for OpenStack: ``OpenStack QCOW2``, ``OpenStack VMDK``, ``OpenStack VDI`` or ``OpenStack VHD``. To get the available builder type, please refer to :ref:`command-line-format`
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
  * ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail. 

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for OpenStack: ``OpenStack QCOW2``, ``OpenStack VMDK``, ``OpenStack VDI`` or ``OpenStack VHD``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing the OpenStack cloud account information required to publish the built machine image.
* ``displayName`` (mandatory): a string providing the name of the image that will be displayed.
* ``tenantName`` (mandatory for keystone v2.0): a string providing the name of the tenant to register the machine image to.  This value is ony required if the cloud account's ``keystoneVersion`` is ``v2.0``
* ``keystoneDomain`` (mandatory for keystone v3.0): a string providing the keystone domain to publish this machine image to.
* ``keystoneProject`` (mandatory for keystone v3.0): a string providing the keystone project to publish this machine image to.
* ``publicImage`` (optional): a boolean to determine if the machine image is public (for other users to use for provisioning).

Deploying a Published Machine Image
-----------------------------------

To deploy a published machine image to OpenStack the OpenStack builder section must have the following definition when using YAML:

.. code-block:: yaml

  ---
  provisioner:
    type: OpenStack
    name: MyDeploy
    region: GRA1
    network: Ext-Net
    flavor: vps-ssd-2

If you are using JSON:

.. code-block:: javascript

  {
    "provisioner": {
      "type": "OpenStack",
      "name": "MyDeploy",
      "region": "GRA1",
      "network": "Ext-Net",
      "flavor": "vps-ssd-2"
    }
  }


The valid keys are:

* ``type`` (mandatory): a string providing the cloud provider on which the published image should be deployed.
* ``name`` (mandatory): the name of the published machine image
* ``region`` (mandatory): the Cloud region 
* ``network`` (mandatory): OpenStack network address
* ``flavor`` (mandatory): the OpenStack flavor defines the compute, memory, and storage capacity of your instance.

OpenStack Cloud Account
-----------------------

Key: ``account``

Used to authenticate the OpenStack platform.

The OpenStack cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for Openstack is ``OpenStack``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``glanceUrl`` (mandatory): a string providing the API URL endpoint of the OpenStack glance service. For example: http://www.example.com/v1/
* ``keystoneUrl`` (mandatory): a string providing the URL endpoint for the OpenStack keystone service to authenticate with. For example: http://www.example.com:5000
* ``keystoneVersion`` (mandatory): a string providing the keystone version of the OpenStack platform.  Refer to :ref:`builder-openstack-valid-keystone-versions`  for the valid keystone versions.
* ``login`` (mandatory): a string providing the user for authenticating to keystone for publishing images
* ``password`` (mandatory): a string providing the password for authenticating to keystone for publishing images
* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

.. _builder-openstack-valid-keystone-versions:

Valid Keystone Versions
-----------------------

* ``v2.0``: Keystone version 2.0
* ``3.0`` : Keystone version 3.0

Example
-------

The following example shows an OpenStack builder with all the information to build and publish a machine image to OpenStack.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: OpenStack QCOW2
    account:
      type: OpenStack
      name: My OpenStack Account
      glanceUrl: http://myglanceurl/v1/
      keystoneUrl: http://mykeystoneurl:9292/v1
      keystoneVersion: v2.0
      login: mylogin
      password: mypassword
    displayName: OpenStack_testHammr
    tenantName: mytenant

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "OpenStack QCOW2",
        "account": {
          "type": "OpenStack",
          "name": "My OpenStack Account",
          "glanceUrl": "http://myglanceurl/v1/",
          "keystoneUrl": "http://mykeystoneurl:9292/v1",
          "keystoneVersion": "v2.0",
          "login": "mylogin",
          "password": "mypassword"
        },
        "displayName": "OpenStack_testHammr",
        "tenantName": "mytenant"
      }
    ]
  }

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``openstack-account.yml``.

.. code-block:: yaml

  ---
  accounts:
  - type: OpenStack
    name: My OpenStack Account
    glanceUrl: http://myglanceurl/v1/
    keystoneUrl: http://mykeystoneurl:9292/v1
    keystoneVersion: http://mykeystoneversion:5000/v2.0
    login: mylogin
    password: mypassword


If you are using JSON, create a JSON file ``openstack-account.json``:

.. code-block:: json

  {
    "accounts": [
      {
        "type": "OpenStack",
        "name": "My OpenStack Account",
        "glanceUrl": "http://myglanceurl/v1/",
        "keystoneUrl": "http://mykeystoneurl:9292/v1",
        "keystoneVersion": "http://mykeystoneversion:5000/v2.0",
        "login": "mylogin",
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
  - type: OpenStack QCOW2
    account:
      file: "/path/to/openstack-account.yml"
    displayName: OpenStack_testHammr
    tenantName: mytenant

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "OpenStack QCOW2",
        "account": {
              "file": "/path/to/openstack-account.json"
        },
        "displayName": "OpenStack_testHammr",
        "tenantName": "mytenant"
      }
    ]
  }

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: OpenStack QCOW2
    account:
      name: My OpenStack Account
    displayName: OpenStack_testHammr
    tenantName: mytenant

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "OpenStack QCOW2",
        "account": {
          "name": "My OpenStack Account"
          },
        "displayName": "OpenStack_testHammr",
        "tenantName": "mytenant"
      }
    ]
  }