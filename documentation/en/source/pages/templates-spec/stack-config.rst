.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-config:

config
======

Within a ``stack``, the ``config`` sub-section describes boot scripts to be added to the template and executed as part of the boot sequence of an instance.

The definition of a ``config`` section when using YAML is:

.. code-block:: yaml

	---
	config:
	- # the list of configuration file definitions goes here.

If you are using JSON:

.. code-block:: javascript

	"config": [
	    ...the list of configuration file definitions goes here.
	]

The valid keys to use within a config are:

* ``frequency`` (mandatory): a string to determine when the boot script should be executed. There are only two valid values, firstboot to specify the script should only be executed once on the first time the instance is booted; everyboot to specify the script should be executed every time the instance is booted.
* ``name`` (mandatory): a string providing the name of the boot script.
* ``source`` (mandatory): a string providing the location of the boot script. This can be a filesystem pathname (relative or absolute) or an URL.
* ``type`` (mandatory): a string providing the script type. For the moment the only valid value is bootscript
* ``order`` (optional): an integer providing the boot order.

Example
-------

The following example shows the declaration of two boot scripts, one to be execute only once the first time the machine is instantiated; the second to be executed every time the instance is rebooted.

If you are using YAML:

.. code-block:: yaml

	---
	config:
	- name: configure-mysql.sh
	  source: "/home/joris/demo/configure-mysql.sh"
	  type: bootscript
	  frequency: firstboot
	- name: check-stats.sh
	  source: http://downloads.mysite.com/config/check-stats.sh
	  type: bootscript
	  frequency: everyboot
	  order: '1'

If you are using JSON:

.. code-block:: json

	{
	  "config": [
	    {
	      "name": "configure-mysql.sh",
	      "source": "/home/joris/demo/configure-mysql.sh",
	      "type": "bootscript",
	      "frequency": "firstboot"
	    },
	    {
	      "name": "check-stats.sh",
	      "source": "http://downloads.mysite.com/config/check-stats.sh",
	      "type": "bootscript",
	      "frequency": "everyboot",
	      "order": "1"
	    }
	  ]
	}
