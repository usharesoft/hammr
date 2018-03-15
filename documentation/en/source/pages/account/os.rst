.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _operating-systems:

Operating Systems
=================

Hammr allows you to create machine images for a number of OSes. The type of OS you want to use needs to be defined in the ``os`` section of the configuration file, as described in.

For a list of the OSes that can be added to your template, run ``os list``, for example

.. code-block:: shell

	$ hammr os list
	Getting distributions for [root] ...
	+-----+---------+--------------+--------------+---------------------+--------------------------+
	| Id  |  Name   |   Version    | Architecture |    Release Date     |         Profiles         |
	+=====+=========+==============+==============+=====================+==========================+
	| 120 | CentOS  | 6            | x86_64       | 2011-07-03 02:06:43 | Server                   |
	|     |         |              |              |                     | Minimal                  |
	|     |         |              |              |                     | Minimal Desktop          |
	+-----+---------+--------------+--------------+---------------------+--------------------------+
	| 121 | CentOS  | 6            | i386         | 2011-07-03 04:02:09 | Minimal                  |
	|     |         |              |              |                     | Server                   |
	|     |         |              |              |                     | Minimal Desktop          |
	+-----+---------+--------------+--------------+---------------------+--------------------------+
	| 122 | CentOS  | 5            | x86_64       | 2008-06-19 13:56:25 | Minimal Desktop          |
	|     |         |              |              |                     | Minimal                  |
	|     |         |              |              |                     | Server                   |
	+-----+---------+--------------+--------------+---------------------+--------------------------+
	| 123 | CentOS  | 5            | i386         | 2008-06-19 14:01:21 | Minimal                  |
	|     |         |              |              |                     | Minimal Desktop          |
	|     |         |              |              |                     | Server                   |
	+-----+---------+--------------+--------------+---------------------+--------------------------+
	| 42  | Debian  | 6            | x86_64       | 2010-04-20 00:18:34 | Minimal Desktop          |
	|     |         |              |              |                     | Server                   |
	|     |         |              |              |                     | Minimal                  |
	+-----+---------+--------------+--------------+---------------------+--------------------------+
	| 125 | Debian  | 7            | x86_64       | 2012-11-05 11:17:46 | Minimal Desktop          |
	|     |         |              |              |                     | Server                   |
	|     |         |              |              |                     | Minimal                  |
	+-----+---------+--------------+--------------+---------------------+--------------------------+
	| 124 | Debian  | 7            | i386         | 2012-11-05 11:17:46 | Server                   |
	|     |         |              |              |                     | Minimal                  |
	|     |         |              |              |                     | Minimal Desktop          |
	+-----+---------+--------------+--------------+---------------------+--------------------------+
	Found 7 distributions
