.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-suse-cloud:

Suse Cloud
==========

Default builder type: ``SUSE Cloud``

Require Cloud Account: Yes

`SuseCloud <https://www.suse.com/products/suse-cloud/>`_

The SuseCloud builder provides information for building and publishing the machine image to the SuseCloud cloud platform. The SuseCloud builder requires cloud account information to upload and register the machine image to the SuseCloud platform.
This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The SuseCloud builder section has the following definition when using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Suse Cloud
		# the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "SUSE Cloud",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Suse Cloud: ``SUSE Cloud``. To get the available builder type, please refer to :ref:`command-line-format`
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Suse Cloud: ``SUSE Cloud``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing the SuseCloud cloud account information required to publish the built machine image.
* ``description`` (optional): an object providing the description of the machine image.
* ``imageName`` (mandatory): a string providing the name of the image that will be displayed.
* ``keystoneDomain`` (mandatory for keystone v3.0): a string providing the keystone domain to publish this machine image to.
* ``keystoneProject`` (mandatory for keystone v3.0): a string providing the keystone project to publish this machine image to.
* ``paraVirtMode`` (optional) a boolean to determine if the machine should be provisioned in para-virtualised mode. By default, machine images are provisioned in full-virtualised mode
* ``publicImage`` (optional): a boolean to determine if the machine image is public (for other users to use for provisioning).
* ``tenant`` (mandatory for keystone v2.0): a string providing the name of the tenant to register the machine image to.  This value is ony required if the cloud account's ``keystoneVersion`` is ``v2.0``

SuseCloud Cloud Account
-----------------------

Key: ``account``
Used to authenticate the SuseCloud platform.

The SuseCloud cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Suse Cloud, ``Suse Cloud``. To get the available builder type, please refer to :ref:`command-line-format`
* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.
* ``endpoint`` (mandatory): a string providing the API URL endpoint of the SuseCloud glance service. For example: http://www.example.com:9292
* ``keystoneEndpoint`` (mandatory): a string providing the URL endpoint for the SuseCloud keystone service to authenticate with. For example: http://www.example.com:5000
* ``keystoneVersion`` (mandatory): a string providing the keystone version of the SuseCloud platform.  Refer to :ref:`builder-suse-valid-keystone-versions`  for the valid keystone versions.
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``password`` (mandatory): a string providing the password for authenticating to keystone for publishing images
* ``username`` (mandatory): a string providing the user for authenticating to keystone for publishing images

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

.. _builder-suse-valid-keystone-versions:

Valid Keystone Versions
-----------------------

* ``v2.0``: Keystone version 2.0
* ``3.0`` : Keystone version 3.0

Example
-------

The following example shows a SuseCloud builder with all the information to build and publish a machine image to SuseCloud.

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Suse Cloud
	  account:
	    type: Suse Cloud
	    name: My SuseCloud Account
	    endpoint: http://ow2-04.xsalto.net:9292/v1
	    keystoneEndpoint: http://ow2-04.xsalto.net:5000/v2.0
	    username: test
	    password: password
	  tenant: opencloudware
	  imageName: joris-test
	  description: CentOS Core template.

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Suse Cloud",
	      "account": {
	        "type": "Suse Cloud",
	        "name": "My SuseCloud Account",
	        "endpoint": "http://ow2-04.xsalto.net:9292/v1",
	        "keystoneEndpoint": "http://ow2-04.xsalto.net:5000/v2.0",
	        "username": "test",
	        "password": "password"
	      },
	      "tenant": "opencloudware",
	      "imageName": "joris-test",
	      "description": "CentOS Core template."
	    }
	  ]
	}

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``susecloud-account.yml``.

.. code-block:: yaml

	---
	accounts:
	- type: Suse Cloud
	  name: My SuseCloud Account
	  endpoint: http://ow2-04.xsalto.net:9292/v1
	  keystoneEndpoint: http://ow2-04.xsalto.net:5000/v2.0
	  username: test
	  password: password

If you are using JSON, create a JSON file ``susecloud-account.json``:

.. code-block:: json

	{
	  "accounts": [
	    {
	        "type": "Suse Cloud",
	        "name": "My SuseCloud Account",
	        "endpoint": "http://ow2-04.xsalto.net:9292/v1",
	        "keystoneEndpoint": "http://ow2-04.xsalto.net:5000/v2.0",
	        "username": "test",
	        "password": "password"
	    }
	  ]
	}

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Suse Cloud
	  account:
	    file: "/home/joris/accounts/susecloud-account.yml"
	  tenant: opencloudware
	  imageName: joris-test
	  description: CentOS Core template.

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Suse Cloud",
	      "account": {
	        "file": "/home/joris/accounts/susecloud-account.json"
	      },
	      "tenant": "opencloudware",
	      "imageName": "joris-test",
	      "description": "CentOS Core template."
	    }
	  ]
	}

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

	---
	builders:
	- type: Suse Cloud
	  account:
	    name: My SuseCloud Account
	  tenant: opencloudware
	  imageName: joris-test
	  description: CentOS Core template.

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "Suse Cloud",
	      "account": {
	        "name": "My SuseCloud Account"
	      },
	      "tenant": "opencloudware",
	      "imageName": "joris-test",
	      "description": "CentOS Core template."
	    }
	  ]
	}
