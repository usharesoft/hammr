.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-installation-nics:

nics
====

The following is a list of all the accepted values that can be used for the internet settings mode in an :ref:`stack-installation` sub-section of the stack.

For example:

.. code-block:: javascript

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

* nics: list of nics objects, each nic has:
	- name: connection name.
	- type: nic type only "Ethernet" supported for now.
	- order(optional): nic's order (1,2,3,...) if all nics do not have order their order in the list will be taken.
	- autoConnect: true/false. optional field default value (true).
	- ipv4: ipv4 method [dhcp/static/disabled]
	- ipv6: ipv6 method [dhcp/static/disabled]
	- ipAddresses: list of ip addresses, each ipAddress has:
		- version: IP version 4 / 6
		- address: the ip address
		- netmask: the network mask
		- gateway: the gateway
