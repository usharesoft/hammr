.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _migration:

Migration
=========

The migration section describes the name, OS, source and target information required to migrate a live system.

The definition of a ``migration`` section when using YAML is:

.. code-block:: yaml

	---
	migration:
	  # the migration definition goes here

If you are using JSON:

.. code-block:: javascript

	{
		"migration": {
		    ...the migration definition goes here.
		}
	}

The valid keys to use within a migration are:

* ``name`` (mandatory): a string providing the name of the migration.
* ``os`` (mandatory): a string providing the operating system (linux).
* ``source`` (mandatory): an object describing the live system to migrate.
* ``target`` (mandatory): an object describing the targeted cloud provider.

Sub-Sections
------------

The ``migration`` sub-sections are:

.. toctree::
   :titlesonly:

   migration-source
   migration-destination

Examples
--------

In YAML:

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
	        }
	      }
	    }
	  }
	}
