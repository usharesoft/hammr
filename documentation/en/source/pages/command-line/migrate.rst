.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _command-line-migrate:

migration
=========

Manages all the migrations executed on live systems. The usage is:

.. code-block:: shell

	usage: hammr migration [sub-command] [options]


Sub Commands
------------

``list`` sub-command
~~~~~~~~~~~~~~~~~~~~

Displays all the migrations for the user.

``launch`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Executes an automated migration (including scan, generate and publish) of a running system, based on a YAML or JSON file. The options are:

	* ``--file`` (mandatory): a yaml or json file which specifies the details of the migration to be executed

The file should have the following format in yaml:

.. code-block:: yaml

	---
	migration:
	  name:              myMigration
	  os:                linux
	  source:
	    host:            10.1.2.42
	    ssh-port:        22
	    user:            root
	    password:        welcome
	  target:
	    builder:
	      type:        VMware vCenter
	      displayName:     weasel-vcenter
	      esxHost:         esx4dev.hq.usharesoft.com
	      datastore:       esx4dev_data1_secure
	      network:         VM Network
	      account:
	        name:          weasel
	      hardwareSettings:
	        memory:          1024

In JSON:

.. code-block:: json

	{
	  "migration": {
	    "name": "myMigration",
	    "os": "linux",
	    "source": {
	      "host": "10.0.0.211",
	      "ssh-port": 22,
	      "user": "<user>",
	      "password": "<password>"
	    },
	    "target": {
	      "builder": {
	        "type": "VMware vCenter",
	        "displayName": "weasel-vcenter",
	        "esxHost": "esx4dev.hq.usharesoft.com",
	        "datastore": "esx4dev_data1_secure",
	        "network": "VM Network",
	        "account": {
	          "name": "weasel"
	        },
            "hardwareSettings": {
              "memory": 1024
            }
	      }
	    }
	  }
	}


``delete`` sub-command
~~~~~~~~~~~~~~~~~~~~~~

Deletes a completed migration. The options are:

	* ``--id`` (mandatory): the ID of the migration to delete
