.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-installation-internet:

internetSettings
================

Within an :ref:`stack-installation`, the ``internetSettings`` sub-section describes information for the internet connections. If no information is provided, when an instance is provisioned from the machine image, the ``basic`` option is setup with one Ethernet card with dhcp configured.

If you are using JSON, the following is an example with multi-nics setup:

.. code-block:: javascript

	{
  "stack" : {
    "name" : "MyTemplate",
    "version" : "1.0",
    "installation" : {
      "internetSettings" : "configure",
      "nics" : [
        {
          "name" : "nic_1",
          "type" : "ETHERNET",
          "order" : 1,
          "autoConnect" : "true",
          "ipv4" : "dhcp",
          "ipv6" : "disabled"
        },
        {
          "name" : "nic_2",
          "type" : "ETHERNET",
          "order" : 2,
          "autoConnect" : "true",
          "ipv4" : "static",
          "ipv6" : "disabled",
          "ipAddresses" : [
            {
              "version" : 4,
              "address" : "10.0.0.111",
              "netmask" : "255.255.255.0",
              "gateway" : "10.0.0.1"
            }
          ]
        }
      ],
      "diskSize" : 12288,
      "swapSize" : 512
    },
    "os" : {
      "name" : "CentOS",
      "version" : "7",
      "arch" : "x86_64",
      "profile" : "Minimal"
    }


The valid keys to use within ``internetSettings`` are:

* basic: one Ethernet card with dhcp configured.
* ask: ask during installation.
* configure: nics to be configured in the template. If no nics definitions found in the json or yaml file, will get a bad request error.
* no value: considered as basic.


Sub-sections
------------

The internetSettings sub-sections are:

.. toctree::
   :titlesonly:

   stack-installation-nics
  
