.. Copyright (c) 2007-2017 UShareSoft, All rights reserved

.. _install-compatibility:

Install compatibility
=====================

Table of compatibility between versions of Hammr, UForge_python_sdk and UForge:

	+-----------------+-----------------------------+------------------+
	|  Hammr version  |  UForge_python_sdk version  |  UForge version  |
	+=================+=============================+==================+
	|      3.7-2      |            3.7-2            |      3.7-2       |
	+-----------------+-----------------------------+------------------+


If your hammr version is not compatible with UForge version that you want to reach, hammr will raise an error message with the UForge version:

.. code-block:: shell

	$ hammr --url https://uforge.usharesoft.com/api -u username -p password
	ERROR: Sorry but this version of Hammr (version = 'HAMMR_VERSION') is not compatible with the version of UForge (version = 'UFORGE_VERSION').
	ERROR: Please go to documentation, 'Install compatibility' section, to know how to install a compatible version of Hammr.


To install the good version of Hammr, please run the command below indicating HAMMR-VERSION you want:

.. code-block:: shell
	
	$ pip install hammr==HAMMR-VERSION

