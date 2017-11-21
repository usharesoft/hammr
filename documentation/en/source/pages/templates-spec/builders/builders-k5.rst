.. Copyright (c) 2007-2017 UShareSoft, All rights reserved

.. _builder-k5:

Fujitsu K5
==========

Default builder type: ``Fujitsu K5``

Require Cloud Account: Yes

`www.fujitsu.com/global/solutions/cloud/k5 <http://www.fujitsu.com/global/solutions/cloud/k5/>`_

The K5 builder provides information for building and publishing the machine image to the Fujitsu K5 cloud platform. This builder supports only VMDK (``Fujitsu K5``) based images for K5.
This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder type, please refer to :ref:`command-line-format`.

The K5 builder requires cloud account information to upload and register the machine image to the K5 platform.

The K5 builder section has the following definition when using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Fujitsu K5
    # the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "Fujitsu K5",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for K5: ``Fujitsu K5``. To get the available builder type, please refer to :ref:`command-line-format`.
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:

  * ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for K5: ``Fujitsu K5``. To get the available builder type, please refer to :ref:`command-line-format`.
* ``account`` (mandatory): an object providing the K5 cloud account information required to publish the built machine image.
* ``displayName`` (mandatory): a string providing the name of the image that will be displayed.
* ``domain`` (mandatory): a string providing the K5 domain to publish this machine image to.
* ``project`` (mandatory): a string providing the K5 project to publish this machine image to.
* ``region`` (mandatory): a string providing the region where to publish the machine image. See below for valid regions.

Valid Regions
-------------

The following regions are supported:

* ``uk-1``: United Kingdom Region 1
* ``jp-east-1``: Eastern Japan Region 1
* ``jp-west-1``: Western Japan Region 1
* ``jp-west-2``: Western Japan Region 2

K5 Cloud Account
-----------------------

Key: ``account``

Used to authenticate the K5 platform.

The K5 cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for K5 is ``K5``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``login`` (mandatory): a string providing the user for authenticating to keystone for publishing images
* ``password`` (mandatory): a string providing the password for authenticating to keystone for publishing images
* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.


Example
-------

The following example shows a K5 builder with all the information to build and publish a machine image to K5.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Fujitsu K5
    account:
      type: K5
      name: My K5 Account
      login: mylogin
      password: mypassword
    displayName: K5_testHammr
    domain: mydomain
    project: myproject
    region: uk-1

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Fujitsu K5",
        "account": {
          "type": "K5",
          "name": "My K5 Account",
          "login": "mylogin",
          "password": "mypassword"
        },
        "displayName": "K5_testHammr",
        "domain": "mydomain",
        "project": "myproject",
        "region": "uk-1"
      }
    ]
  }

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``k5-account.yml``.

.. code-block:: yaml

  ---
  accounts:
  - type: K5
    name: My K5 Account
    login: mylogin
    password: mypassword


If you are using JSON, create a JSON file ``k5-account.json``:

.. code-block:: json

  {
    "accounts": [
      {
        "type": "K5",
        "name": "My K5 Account",
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
  - type: Fujitsu K5
    account:
      file: "/path/to/k5-account.yml"
    displayName: K5_testHammr
    domain: mydomain
    project: myproject
    region: uk-1

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Fujitsu K5",
        "account": {
              "file": "/path/to/k5-account.json"
        },
        "displayName": "K5_testHammr",
        "domain": "mydomain",
        "project": "myproject",
        "region": "uk-1"
      }
    ]
  }

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Fujitsu K5
    account:
      name: My K5 Account
    displayName: K5_testHammr
    domain: mydomain
    project: myproject
    region: uk-1

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Fujitsu K5",
        "account": {
          "name": "My K5 Account"
          },
        "displayName": "K5_testHammr",
        "domain": "mydomain",
        "project": "myproject",
        "region": "uk-1"
      }
    ]
  }
