.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _pkgs-updates:

Understanding Package Updates
=============================

A more complete example for adding CentOS is provided below. You will notice the following optional information has been added:

* ``updateTo``: This is the date up until which the packages should be updated
* ``profile``: The OS profile. The options are listed under os list

If you are using YAML:

.. code-block:: yaml

  ---
  os:
    name: CentOS
    version: '6.4'
    arch: x86_64
    updateTo: 01-30-2014
    profile: Minimal
    pkgs:
    - name: iotop
    - name: httpd
      version: 2.2.15
      release: 28.el6.centos
      arch: x86_64

If you are using JSON:

.. code-block:: json

  {
    "os" : {
      "name" : "CentOS",
      "version" : "6.4",
      "arch" : "x86_64",
      "updateTo" : "01-30-2014",
      "profile" : "Minimal",
      "pkgs" : [ {
        "name" : "iotop"
      },
      {
        "name" : "httpd",
        "version" : "2.2.15",
        "release" : "28.el6.centos",
        "arch" : "x86_64"
      }]
    }
  }

In the example above you can see that for the package httpd a specific version and release are specified. When no version or release is specified, the latest release is used.
