.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _pkg-sticky:

Pinning a Package
=================

Being able to roll-forward or roll-back the packages is all well and good, but what if we wanted to force a particular version of a package to be part of the machine image?

Due to the current package version calculation being based on a particular date it is impossible to specify a particular package version to be part of the generation, as depending upon the build date of the package, potentially an earlier or more up to date version of the package may be chosen instead. To get around this issue, hammr provides a mechanism to force a particular package version. This is known as “pinning” a package (previously referred to as macking a package “sticky”). To do this, specify the fullname of the package, or its version, revision and architecture.

For example when using YAML:

.. code-block:: yaml

    ---
    stack:
      name: CentOS Base Template
      version: '6.4'
      description: This is a CentOS core template.
      os:
        name: CentOS
        version: '6.4'
        arch: x86_64
        profile: Minimal
        updateTo: '2013-06-15'
        pkgs:
        - name: php
          version: 5.5.3
          release: 23.el6_4
          arch: i686
        - name: php-common
          fullName: php-common-5.5.3-23.el6_4-i686.rpm

If you are using JSON:

.. code-block:: json

	{
	  "stack": {
	    "name": "CentOS Base Template",
	    "version": "6.4",
	    "description": "This is a CentOS core template.",
	    "os": {
	      "name": "CentOS",
	      "version": "6.4",
	      "arch": "x86_64",
	      "profile": "Minimal",
	      "updateTo": "2013-06-15",
	      "pkgs": [
	        {
	          "name": "php",
	          "version": "5.5.3",
	          "release": "23.el6_4",
	          "arch": "i686"
	        },
	        {
	          "name": "php-common",
	          "fullName": "php-common-5.5.3-23.el6_4-i686.rpm"
	        }
	      ]
	    }
	  }
	}
