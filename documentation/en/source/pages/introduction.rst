.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _intro-tag:

Introduction
============

Hammr is an open source tool for creating machine images for different environments from a single configuration file, or migrating live systems from one environment to another. Hammr is a lightweight client-side tool based on Python, and can be installed on all major operating systems.

A machine image contains a set of operating system packages and other 3rd party software required to run a particular service. Once a machine image is created, it can be used to provision one or more identical running instances. The format of the machine image varies depending on whether you want to run your service on a physical machine (e.g ISO) a virtual datacenter (e.g OVF for VMware vCenter) or cloud environment (e.g. AMI for Amazon EC2).

Hammr can be used as part of your "DevOps tool chain" and in conjunction with other tools such as Jenkins, Chef, Puppet and SaltStack, allowing you to easily build your machine images and maintain your live running instances.  Hammr also has migration capabilities, allowing you to scan a live system, generate a machine image for a different environment as well as export it back to a configuration file for sharing.

.. warning: Hammr provides a local interface with a UForge Server. The UForge Server can be an `on-premise installation <https://www.usharesoft.com/products/appcenter.html>`_ or in `SaaS <https://www.usharesoft.com/products/uforgenow.html>`_. If you don’t have a UForge Server, then you can get a free online account `here <https://www.usharesoft.com/signup/signup.html>`_.