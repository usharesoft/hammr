.. Copyright (c) 2007-2019 UShareSoft, All rights reserved

.. _builder-openshift:

OpenShift
=========

Default builder type: ``OpenShift``

Require Cloud Account: Yes

`https://manage.openshift.com/ <https://manage.openshift.com/>`_

The OpenShift builder provides information for building and publishing machine images for OpenShift Online or OpenShift Origin. The OpenShift builder requires cloud account information to upload and register the machine image to OpenShift cloud.
This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The OpenShift builder section has the following definition when using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: OpenShift
    # the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "OpenShift",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for OpenShift: ``OpenShift``. To get the available builder type, please refer to :ref:`command-line-format`.
* ``entrypoint`` (mandatory): a string describing the command to launch at OpenShift container start in ``exec`` form.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for OpenShift: ``OpenShift``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing the OpenShift cloud account information required to publish the built machine image.
* ``namespace`` (mandatory): a string providing the OpenShift namespace to publish this machine image to.
* ``repositoryName`` (mandatory): a string providing the OpenShift repository name of the image.
* ``tagName`` (mandatory): a string providing the OpenShift tag name of the image.

OpenShift Cloud Account
-----------------------

Key: ``account``

Used to authenticate the OpenShift Registry.

The OpenShift cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for OpenShift is ``OpenShift``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``registryUrl`` (mandatory): a string providing the endpoint URL of the OpenShift Registry.
* ``token`` (mandatory): a string providing the token of the user for authenticating to the OpenShift platform for publishing images
* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows an OpenShift builder with all the information to build and publish a machine image to OpenShift Online.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: OpenShift
    entrypoint: [\"/bin/sh\"]
    account:
      type: OpenShift
      name: myOpenShiftaccount
      registryUrl: https://myopenshiftregistry.com
      token: mytoken
    namespace: mynamespace
    repositoryName: myrepositoryname
    tagName: latest

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "OpenShift",
        "entrypoint": "[\"/bin/sh\"]",
        "account": {
          "type": "OpenShift",
          "name": "myOpenShiftaccount",
          "registryUrl:": "https://myopenshiftregistry.com",
          "token:": "mytoken:"
        },
        "namespace": "mynamespace",
        "repositoryName": "myrepositoryname",
        "tagName": "latest"
      }
    ]
  }

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``openshift-account.yml``.

.. code-block:: yaml

  ---
  accounts:
  - type: OpenShift
    name: OpenShiftAccount
    registryUrl: https://myopenshiftregistry.com
    token: mytoken


If you are using JSON, create a JSON file ``openshift-account.json``:

.. code-block:: json

  {
    "accounts": [
      {
        "type": "OpenShift",
        "name": "OpenShiftAccount",
        "registryUrl": "https://myopenshiftregistry.com",
        "token": "mytoken"
      }
    ]
  }

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: OpenShift
    entrypoint: [\"/bin/sh\"]
    account:
      file: "/path/to/openshift-account.yml"
    namespace: mynamespace
    repositoryName: myrepositoryname
    tagName: latest

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "OpenShift",
        "entrypoint": "[\"/bin/sh\"]",
        "account": {
              "file": "/path/to/openshift-account.json"
        },
        "namespace": "mynamespace",
        "repositoryName": "myrepositoryname",
        "tagName": "latest"
      }
    ]
  }

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: OpenShift
    entrypoint: [\"/bin/sh\"]
    account:
      name: OpenShift account
    namespace: mynamespace
    repositoryName: myrepositoryname
    tagName: latest

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "OpenShift",
        "entrypoint": "[\"/bin/sh\"]",
        "account": {
          "name": "OpenShift account"
          },
        "namespace": "mynamespace",
        "repositoryName": "myrepositoryname",
        "tagName": "latest"
      }
    ]
  }

