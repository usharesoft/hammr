.. Copyright (c) 2007-2017 UShareSoft, All rights reserved

.. _builder-oracle-cloud:

Oracle Cloud
============

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