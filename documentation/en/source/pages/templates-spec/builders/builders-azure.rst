.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _builder-azure:

Microsoft Azure
===============

Default builder type: ``Microsoft Azure``

Require Cloud Account: Yes

`azure.microsoft.com <http://azure.microsoft.com>`_

The Azure builder provides information for building and publishing the machine image to the Microsoft Azure cloud platform.
This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder types, please refer to :ref:`command-line-format`

The Azure builder section has the following definition when using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Microsoft Azure
    # the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "Microsoft Azure",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Azure: ``Microsoft Azure``. To get the available builder type, please refer to :ref:`command-line-format`
* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the stack section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the :ref:`template-stack`. This cannot be used if an advanced partitioning table is defined in the stack.

.. note:: When building from a scan, your yaml or json file must contain an ``installation`` section in ``builders``. This is mandatory when you create a new template, but might be missing when you build from a scan. Make sure it is present or your build will fail.



Publishing a Machine Image with Azure Resource Manager Connector
----------------------------------------------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Azure: ``Microsoft Azure``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing all the cloud account information to authenticate and publish a machine image to Azure.
* ``storageAccount`` (mandatory): a string providing the storage account to use for uploading and storing the machine image. The storage account is the highest level of the namespace for accessing each of the fundamental services.
* ``container`` (mandatory): the container that will contains the blob file in Azure Cloud. If the names provides doesn't already exist it will be created.
* ``blob`` (mandatory): the name of the vhd blob that will contains the machine image data. It must ends with ".vhd". If it already exists it will be overrride.
* ``displayName`` (mandatory): a string providing the name of the machine image to display in Azure cloud. If it already exists it will be overrride.
* ``resourceGroup`` (optional): an existing resource group available in your clound accound. By default the resource group of your storage account will be used.


Azure Resource Manager Cloud Account
------------------------------------

Key: ``account``

Used to authenticate the Azure platform.
The Azure Resource Manager cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for Microsoft Azure: ``Microsoft Azure``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``tenantId`` (mandatory): The tenant ID also named "Directory ID". See azure documentation to retrieves yours: https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-create-service-principal-portal#get-tenant-id
* ``applicationId`` (mandatory): The application ID that will be used by UForge. See azure documentation to create one application: https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-create-service-principal-portal#get-application-id-and-authentication-key
* ``applicationPassword`` (mandatory): The application authentication key associated to the application ID.

.. note:: In the case where name or file is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows an Azure builder with all the information to build and publish a machine image to Azure.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Microsoft Azure
    account:
      type: Microsoft Azure
      name: My Azure Resource Manager account
      tenantId: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeeee
      applicationId: 0000000-1111-2222-3333-4444444444444
      applicationPassword: myApplicationPassword
    storageAccount: mystorageaccount
    container: mycontainer
    resourceGroup: myResourceGroup
    blob: myBlob.vhd
    displayName: myImage

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Microsoft Azure",
        "account": {
          "type": "Microsoft Azure",
          "name": "My Azure Resource Manager account",
          "tenantId": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeeee",
          "applicationId": "0000000-1111-2222-3333-4444444444444",
          "applicationPassword": "myApplicationPassword"
        },
        "storageAccount":"mystorageaccount",
        "container":"mycontainer",
        "resourceGroup":"myResourceGroup",
        "blob":"myBlob.vhd",
        "displayName":"myImage"
      }
    ]
  }

Referencing the Azure Resource Manager Cloud Account
----------------------------------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``azure-app-account.yml``.

.. code-block:: yaml

  ---
  accounts:
  - type: Microsoft Azure
    name: My Azure Resource Manager account
    tenantId: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeeee
    applicationId: 0000000-1111-2222-3333-4444444444444
    applicationPassword: myApplicationPassword


If you are using JSON, create a JSON file ``azure-app-account.json``:

.. code-block:: json

  {
    "accounts": [
      {
        "type": "Microsoft Azure",
        "name": "My Azure Resource Manager account",
        "tenantId": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeeee",
        "applicationId": "0000000-1111-2222-3333-4444444444444",
        "applicationPassword": "myApplicationPassword"
      }
    ]
  }

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Microsoft Azure
    account:
      file: "/home/user/accounts/azure-app-account.yml"
    storageAccount: mystorageaccount
    container: mycontainer
    resourceGroup: myResourceGroup
    blob: myBlob.vhd
    displayName: myImage

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Microsoft Azure",
        "account": {
              "file": "/home/user/accounts/azure-app-account.json"
        },
        "storageAccount":"mystorageaccount",
        "container":"mycontainer",
        "resourceGroup":"myResourceGroup",
        "blob":"myBlob.vhd",
        "displayName":"myImage"
      }
    ]
  }

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Microsoft Azure
    account:
      name: My Azure Resource Manager Account
    storageAccount: mystorageaccount
    container: mycontainer
    resourceGroup: myResourceGroup
    blob: myBlob.vhd
    displayName: myImage

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Microsoft Azure",
        "account": {
              "name": "My Azure Resource Manager Account"
        },
        "storageAccount":"mystorageaccount",
        "container":"mycontainer",
        "resourceGroup":"myResourceGroup",
        "blob":"myBlob.vhd",
        "displayName":"myImage"
      }
    ]
  }


Publishing a Machine Image with Azure Classic Connector (deprecated)
--------------------------------------------------------------------

To publish an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for Azure: ``Microsoft Azure``. To get the available builder type, please refer to :ref:`command-line-format`
* ``account`` (mandatory): an object providing all the cloud account information to authenticate and publish a machine image to Azure.
* ``region`` (mandatory): a string providing the region where to create the storage account. If the storage account already exists, then you should not specify a region. See below for valid regions.
* ``storageAccount`` (mandatory): a string providing the storage account to use for uploading and storing the machine image. The storage account is the highest level of the namespace for accessing each of the fundamental services.

Valid Azure Regions
---------------------

* ``North Central US``
* ``South Central US``
* ``East US``
* ``West US``
* ``North Europe``
* ``West Europe``
* ``East Asia``

Azure Classic Cloud Account (deprecated)
----------------------------------------

Key: ``account``

Used to authenticate the Azure platform.
The Azure Classic cloud account has the following valid keys:

* ``type`` (mandatory): a string providing the cloud account type. Default platform type for Microsoft Azure: ``Microsoft Azure``. To get the available platform type, please refer to :ref:`command-line-platform`
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``publishsettings`` (mandatory): A string providing the pathname where to retrieve the publish settings and subscription information file. This should be a (.publishsettings) file.
* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.

.. note:: In the case where name or file is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows an Azure builder with all the information to build and publish a machine image to Azure.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Microsoft Azure
    account:
      type: Microsoft Azure
      name: My Azure account
      publishsettings: "/path/to/Pay-As-You-Go-4-25-2016-credentials.publishsettings"
    storageAccount: mystorageaccount
    region: Central US

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Microsoft Azure",
        "account": {
          "type": "Microsoft Azure",
          "name": "My Azure account",
          "publishsettings": "/path/to/Pay-As-You-Go-4-25-2016-credentials.publishsettings"
        },
        "storageAccount":"mystorageaccount",
        "region":"Central US"
      }
    ]
  }

Referencing the Azure Classic Cloud Account (deprecated)
--------------------------------------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a YAML file ``azure-account.yml``.

.. code-block:: yaml

  ---
  accounts:
  - type: Microsoft Azure
    name: My Azure account
    publishsettings: "/path/to/Pay-As-You-Go-date-credentials.publishsettings"


If you are using JSON, create a JSON file ``azure-account.json``:

.. code-block:: json

  {
    "accounts": [
      {
        "type": "Microsoft Azure",
        "name": "My Azure account",
        "publishsettings": "/path/to/Pay-As-You-Go-date-credentials.publishsettings"
      }
    ]
  }

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Microsoft Azure
    account:
      file: "/home/joris/accounts/azure-account.yml"
    storageAccount: mystorageaccount
    region: Central US

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Microsoft Azure",
        "account": {
              "file": "/home/joris/accounts/azure-account.json"
        },
        "storageAccount":"mystorageaccount",
        "region":"Central US"
      }
    ]
  }

Reference by name, note the cloud account must already be created by using ``account create``.

If you are using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: Microsoft Azure
    account:
      name: My Azure Account
    storageAccount: mystorageaccount
    region: Central US

If you are using JSON:

.. code-block:: json

  {
    "builders": [
      {
        "type": "Microsoft Azure",
        "account": {
              "name": "My Azure Account"
        },
        "storageAccount":"mystorageaccount",
        "region":"Central US"
      }
    ]
  }
