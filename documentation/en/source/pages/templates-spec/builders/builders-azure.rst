.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _builder-azure:

Microsoft Azure
===============

Builder type: ``azure``

Require Cloud Account: Yes
`azure.microsoft.com <http://azure.microsoft.com>`_

The Azure builder provides information for building and publishing the machine image to the Microsoft Azure cloud platform.

The Azure builder section has the following definition:

.. code-block:: javascript

	{
	  "builders": [
	    {
	      "type": "azure",
	      ...the rest of the definition goes here.
	    }
	  ]
	}

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``installation`` (optional): an object providing low-level installation or first boot options. These override any installation options in the stack section. The following valid keys for installation are:
	* ``diskSize`` (mandatory): an integer providing the disk size of the machine image to create. Note, this overrides any disk size information in the :ref:`template-stack`. This cannot be used if an advanced partitioning table is defined in the stack.
* ``type`` (mandatory): a string providing the machine image type to build: ``azure``

Publishing a Machine Image
--------------------------

To publish an image, the valid keys are:

* ``account`` (mandatory): an object providing all the cloud account information to authenticate and publish a machine image to Azure.
* ``location`` (optional): a string providing the location where to create the storage account. If the storage account already exists, then you should not specify a location. See below for valid locations.
* ``storageAccount`` (mandatory): a string providing the storage account to use for uploading and storing the machine image. The storage account is the highest level of the namespace for accessing each of the fundamental services.
* ``type`` (mandatory): a string providing the machine image type to build: ``azure``

Valid Azure Locations
---------------------

* ``North Central US``
* ``South Central US``
* ``East US``
* ``West US``
* ``North Europe``
* ``West Europe``
* ``East Asia``

Azure Cloud Account
-------------------

Key: ``account``

Used to authenticate the Azure platform.
The Azure cloud account has the following valid keys:

* ``certKey`` (mandatory): A string providing the pathname or URL where to retrieve the X.509 certificate v3 public key associated with your Azure account. This should be a (.pem) file.
* ``file`` (optional): a string providing the location of the account information. This can be a pathname (relative or absolute) or an URL.
* ``name`` (mandatory): a string providing the name of the cloud account. This name can be used in a builder section to reference the rest of the cloud account information.
* ``rsaPrivateKey`` (mandatory): A string providing the pathname or URL where to retrieve the private RSA key associated with your Azure account. This should be a (.pem) file.
* ``subscriptionId`` (mandatory): A string providing your Axure subscription Id. To get your subscription Id, log into Windows Azure, click on “Settings”. The id is listed in the table.
* ``type`` (mandatory): a string providing the cloud account type: ``azure``.

.. note:: In the case where name or file is used to reference a cloud account, all the other keys are no longer required in the account definition for the builder.

Example
-------

The following example shows an Azure builder with all the information to build and publish a machine image to Azure.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "azure",
	      "account": {
	        "type": "azure",
	        "name": "My Azure Account",
	        "subscriptionId": "xxxbewssbewdsbew-sdsewjwdtg-ssatgh-xxxdft5f323",
	        "certKey": "/home/joris/accounts/azure/cert.pem",
	        "rsaPrivateKey": "/home/joris/accounts/azure/key.pem"
	      },
	      "storageAccount": "mystorageaccount",
	      "location": "West Europe"
	    }
	  ]
	}

Referencing the Cloud Account
-----------------------------

To help with security, the cloud account information can be referenced by the builder section. This example is the same as the previous example but with the account information in another file. Create a json file ``azure-account.json``.

.. code-block:: json

	{
	  "accounts": [
	    {
	        "type": "azure",
	        "name": "My Azure Account",
	        "subscriptionId": "xxxbewssbewdsbew-sdsewjwdtg-ssatgh-xxxdft5f323",
	        "certKey": "/home/joris/accounts/azure/cert.pem",
	        "rsaPrivateKey": "/home/joris/accounts/azure/key.pem"
	    }
	  ]
	}

The builder section can either reference by using ``file`` or ``name``.

Reference by file:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "azure",
	      "account": {
	        "file": "/home/joris/accounts/azure-account.json"
	      },
	      "storageAccount": "mystorageaccount",
	      "location": "West Europe"
	    }
	  ]
	}

Reference by name, note the cloud account must already be created by using ``account create``.

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "abiquo",
	      "account": {
	        "name": "My Abiquo Account"
	      },
	      "storageAccount": "mystorageaccount",
	      "location": "West Europe"
	    }
	  ]
	}
