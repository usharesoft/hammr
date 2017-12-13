.. Copyright (c) 2007-2017 UShareSoft, All rights reserved

.. _builder-oracle-cloud:

Oracle Cloud
============

Default builder type: ``Oracle Cloud``

Require Cloud Account: Yes

`cloud.oracle.com <https://cloud.oracle.com>`_

The Oracle Cloud builder provides information for building and publishing the machine image to the Oracle Cloud platform.

The Oracle Cloud builder requires cloud account information to upload and register the machine image to the Oracle Cloud platform.

The Oracle Cloud builder section has the following definition when using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Oracle Cloud
    # the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

    {
      "builders": [
	    {
	      "type": "Oracle Cloud",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for OpenStack: ``Oracle Cloud``. To get the available builder type, please refer to :ref:`command-line-format`
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the :ref:`template-stack` section. The following valid keys for installation are:
  * ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the stack. This cannot be used if an advanced partitioning table is defined in the stack.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Oracle Cloud: ``Oracle Cloud``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing the Oracle Cloud account information required to publish the built machine image.
* ``displayName`` (mandatory): a string providing the name of the image that will be displayed.
* ``computeEndPoint`` (mandatory): a string providing the compute end point url to register the machine image to.

Oracle Cloud Account
--------------------

Key: ``account``

Used to authenticate the Oracle Cloud platform.

The Oracle Cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for Oracle Cloud is ``Oracle``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``login`` (mandatory): a string providing the user name for authenticating to Oracle Cloud for publishing images
* ``password`` (mandatory): a string providing the password for authenticating to Oracle Cloud for publishing images
* ``domainName`` (mandatory): a string providing the domain for authenticating to Oracle Cloud for publishing images. For example: a123456

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows an Oracle Cloud builder with all the information to build and publish a machine image to Oracle Cloud.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Oracle Cloud
    account:
      type: Oracle
      name: My Oracle Cloud Account
      login: mylogin@example.com
      password: mypassword
      domainName: a123456
    displayName: myOracleDisplayName
    computeEndPoint: myComputeEndPointUrl

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Oracle Cloud",
        "account": {
          "type": "Oracle",
          "name": "My Oracle Cloud Account",
          "login": "mylogin@example.com",
          "password": "mypassword",
          "domainName": "a123456"
        },
        "displayName": "myOracleDisplayName",
        "computeEndPoint": "myComputeEndPointUrl"
      }
    ]
  }

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``oracle-cloud-account.yml``.

.. code-block:: yaml

  ---
  accounts:
  - type: Oracle
    name: My Oracle Cloud Account
    login: mylogin@example.com
    password: mypassword
    domainName: a123456


If you are using JSON, create a JSON file ``oracle-cloud-account.json``:

.. code-block:: json

  {
    "accounts": [
      {
        "type": "Oracle",
        "name": "My Oracle Cloud Account",
        "login": "mylogin@example.com",
        "password": "mypassword",
        "domainName": "a123456"
      }
    ]
  }



The builder section can be references by using either ``file`` or ``name``.

Reference by file:

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Oracle Cloud
    account:
      file: "/path/to/oracle-cloud-account.yml"
    displayName: myOracleDisplayName
    computeEndPoint: myComputeEndPointUrl

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Oracle Cloud",
        "account": {
              "file": "/path/to/oracle-cloud-account.json"
        },
        "displayName": "myOracleDisplayName",
        "computeEndPoint": "myComputeEndPointUrl"
      }
    ]
  }

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Oracle Cloud
    account:
      name: My Oracle Cloud Account
    displayName: myOracleDisplayName
    computeEndPoint: myComputeEndPointUrl

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Oracle Cloud",
        "account": {
              "name": "My Oracle Cloud Account"
        },
        "displayName": "myOracleDisplayName",
        "computeEndPoint": "myComputeEndPointUrl"
      }
    ]
  }
