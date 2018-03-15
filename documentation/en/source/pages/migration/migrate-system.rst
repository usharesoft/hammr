.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _migrating-live-system:

Migrating a Live System
=======================

Hammr allows you to migrate a live system. The key steps in migrating your system are:

1. Scan your system, this sends a scan report back to your UForge account
2. From the scan report, build and publish a machine image
3. Finally provision an instance from the published machine image (effectively migrating the system)

Optionally, at step #2, you can import the scan report to create a template. This allows you to change the content prior to building a machine image.

First, scan the system you wish to migrate by running ``scan run``. This "deep scans" the live system, reporting back the meta-data of every file and package that makes up the running workload. The following is an example of a scan of a live system:

.. note:: The following example shows a simple scan (without overlay). If you would like the overlay, add ``--overlay`` argument to the command.

.. code-block:: shell

	$ hammr scan run --ip 192.0.2.0 --scan-login root --name scan-name
	Password for root@192.0.2.0: 
	... uforge-scan v2.54 (Feb 18 2014 13:16:37) (SVN Revision: 21664)
	... Distribution:        Debian / 6.0.9 / x86_64
	... Current System Name: Linux
	...         Node Name:   test-deb-1-0rev2-vbox
	...         Release:     2.6.32-5-amd64
	...         Version:     #1 SMP Tue May 13 16:34:35 UTC 2014
	...         Machine:     x86_64
	...         Domain:      (none)
	... Server URL: http://192.168.10.141/ufws-3.3
	... User: root
	... Testing connection to the service...
	...                                     SUCCESS!
	... 
	... 
	Searching scan on uforge ...
	|>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>| 100%: Successfully scanned |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<|
	OK: Scan successfully

Once you have run the scan of your system, a scan report is saved to your account. You can list your scans by running ``scan list``. The output will be similar to the following. As you can see below, the “scanExample” is the group name. The actual scan appears below it with “Scan #1“ added to the name. If you run the scan on the same machine again, the scan number will increase. This allows you to compare scans.

.. note:: In this example, “scanExample“ is a simple scan. If it was a scan with overlay an “X“ will appear in the column “With overlay“ for the group name.

.. code-block:: shell

	$ hammr scan list
	Getting scans for [root] ...
	+-----+-----------------------------+--------+-----------------+--------------+
	| Id  |            Name             | Status |  Distribution   | With overlay |
	+=====+=============================+========+=================+==============+
	| 133 | scanExample                 |        | Debian 6 x86_64 |              |
	+-----+-----------------------------+--------+-----------------+--------------+
	| 149 |         scanExample Scan #1 | Done   |                 |              |
	+-----+-----------------------------+--------+-----------------+--------------+
	Found 1 scans

If you are simply moving your system from one cloud provider to another, you can then simply build a machine image from this scan by running ``scan build``. The following is an example which builds a machine image from a scan:

.. code-block:: shell

	$ hammr scan build --id 192 --file openstack-builder.yml
	OK: Syntax of template file [openstack-builder.yml] is ok
	Generating 'openstack' image (1/1)
	|>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>| 100%: Done, created on ... |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<|
	OK: Generation 'openstack' ok

In the example above, you will need to have a YAML file which defines the ``builder`` parameters for the type of machine image you want to create. This is NOT a full template configuration file, but just the builders parameters. For example:

.. code-block:: yaml

	---
	builders:
	- type: openstack
	  hardwareSettings:
	    memory: 1024
	  installation:
	    diskSize: 2000
	  account: Openstack OW2
	  tenant: opencloudware
	  imageName: scan-test
	  publicImage: 'no'

If you are using JSON:

.. code-block:: json

	{
	  "builders": [
	    {
	      "type": "openstack",
	      "hardwareSettings": {
	        "memory": 1024
	      },
	      "installation": {
	        "diskSize": 2000
	      },
	      "account": "Openstack OW2",
	      "tenant": "opencloudware",
	      "imageName": "scan-test",
	      "publicImage": "no"
	    }
	  ]
	}

Updating a Template Before Migrating
------------------------------------

Hammr also allows you to modify or update packages that are part of the system you want to migrate. To do this, you first need to transform the scan report to a template. You can then modify any part of this new template prior to building the final machine image used for migration.

To create a template from your scan you will need to run ``scan import``. The following is an example that shows a scan conversion to a template within UForge.

.. code-block:: shell

	$ hammr scan import --id 123 --name "MyScan" --version "1.0"
	Import scan id [123] ...
	|>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>| 100%: Imported 28 May 2... |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<|
	OK: Importing ok

Once this template is created, you can now update it. In this release, hammr does not provide a mechanism to update existing templates. So to update a template you must:

1. Export the template – see section :ref:`exporting-importing-templates` for more information.
2. Extract the archive, retrieving the configuration file (JSON or YAML).
3. Update the configuration file (JSON or YAML) with the required changes, you will need to change either the template name or version so you do not get a conflict when you create the new template.
4. Create a new template – see section :ref:`creating-managing-templates`.
5. Build and publish the machine image (which effectively migrates the workload with the changes) – see section :ref:`machine-images`


