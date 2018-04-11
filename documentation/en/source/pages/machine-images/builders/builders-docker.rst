.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-docker:

Docker
======

Default builder type: ``Docker``

Require Cloud Account: Yes

`www.docker.com <https://www.docker.com/>`_

The Docker builder provides information for building and publishing the machine image to a Docker Registry.
This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder type, please refer to :ref:`command-line-format`

The Docker builder requires cloud account information to upload and register the machine image to a Docker Registry.

The Docker builder section has the following definition when using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Docker
    # the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

  {
    "builders": [
      {
        "type": "Docker",
        ...the rest of the definition goes here.
      }
    ]
  }

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Docker: ``Docker``. To get the available builder type, please refer to :ref:`command-line-format`.

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Docker: ``Docker``. To get the available builder type, please refer to :ref:`command-line-format`.
* ``account`` (mandatory): an object providing the Docker cloud account information required to publish the built machine image.
* ``namespace`` (mandatory): a string providing the Docker namespace to publish this machine image to.
* ``repositoryName`` (mandatory): a string providing the Docker repository name of the image.
* ``tagName`` (mandatory): a string providing the Docker tag name of the image.

Docker Cloud Account
--------------------

Key: ``account``

Used to authenticate the Docker Registry.

The Docker cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for Docker is ``Docker``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``endpointUrl`` (mandatory): a string providing the endpoint URL of the Docker Registry.
* ``login`` (mandatory): a string providing the login of the user for authenticating to the Docker Registry for publishing images
* ``password`` (mandatory): a string providing the password of the user for authenticating to the Docker Registry for publishing images
* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.

.. note:: In the case where ``name`` or ``file`` is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.


Example
-------

The following example shows a Docker builder with all the information to build and publish a machine image to Docker Hub.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Docker
    account:
      type: Docker
      name: Docker Hub
      endpointUrl: https://index.docker.io
      login: mylogin
      password: mypassword
    namespace: mylogin
    repositoryName: uforge-image
    tagName: latest

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Docker",
        "account": {
          "type": "Docker",
          "name": "Docker Hub",
          "endpointUrl": "https://index.docker.io",
          "login": "mylogin",
          "password": "mypassword"
        },
        "namespace": "mylogin",
        "repositoryName": "uforge-image",
        "tagName": "latest"
      }
    ]
  }

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``docker-account.yml``.

.. code-block:: yaml

  ---
  accounts:
  - type: Docker
    name: Docker Hub
    endpointUrl: https://index.docker.io
    login: mylogin
    password: mypassword


If you are using JSON, create a JSON file ``docker-account.json``:

.. code-block:: json

  {
    "accounts": [
      {
        "type": "Docker",
        "name": "Docker Hub",
        "endpointUrl": "https://index.docker.io",
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
  - type: Docker
    account:
      file: "/path/to/docker-account.yml"
    namespace: mylogin
    repositoryName: uforge-image
    tagName: latest

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Docker",
        "account": {
              "file": "/path/to/docker-account.json"
        },
        "namespace": "mylogin",
        "repositoryName": "uforge-image",
        "tagName": "latest"
      }
    ]
  }

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Docker
    account:
      name: Docker Hub
    namespace: mylogin
    repositoryName: uforge-image
    tagName: latest

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Docker",
        "account": {
          "name": "Docker Hub"
          },
        "namespace": "mylogin",
        "repositoryName": "uforge-image",
        "tagName": "latest"
      }
    ]
  }