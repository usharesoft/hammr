.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _install-compatibility:

Install Compatibility
=====================

The following table lists the compatibility between versions of Hammr, UForge_python_sdk and UForge:

	+-----------------+-----------------------------+------------------+
	|  Hammr version  |  UForge_python_sdk version  |  UForge version  |
	+=================+=============================+==================+
	|      3.7-2      |            3.7-2            |      3.7-2       |
	+-----------------+-----------------------------+------------------+
	|     3.7.2-1     |           3.7.2-1           |    3.7.fp2-1     |
	+-----------------+-----------------------------+------------------+
	|      3.7-3      |            3.7-3            |      3.7-3       |
	+-----------------+-----------------------------+------------------+
	|      3.7.0.5    |            3.7-5            |      3.7-5       |
	+-----------------+-----------------------------+------------------+
	|      3.7.0.6    |            3.7-6            |      3.7-6       |
	+-----------------+-----------------------------+------------------+
	|      3.7.0.7    |            3.7-7            |      3.7-7       |
	+-----------------+-----------------------------+------------------+
	|      3.7.3      |            3.7.3            |      3.7.3       |
	+-----------------+-----------------------------+------------------+
	|      3.7.4      |            3.7.4            |      3.7.4       |
	+-----------------+-----------------------------+------------------+
	|      3.7.5      |            3.7.5            |      3.7.5       |
	+-----------------+-----------------------------+------------------+
	|      3.7.6      |            3.7.6            |      3.7.6       |
	+-----------------+-----------------------------+------------------+
	|      3.7.7      |            3.7.7            |      3.7.7       |
	+-----------------+-----------------------------+------------------+
	|      3.7.8      |            3.7.8            |      3.7.8       |
	+-----------------+-----------------------------+------------------+
	|      3.8.1      |            3.8.1            |      3.8.1       |
	+-----------------+-----------------------------+------------------+


If your hammr version is not compatible with the UForge version that you want to reach, hammr will raise an error message with the UForge version:

.. code-block:: shell

	$ hammr --url https://your-uforge.com/api -u username -p password
	ERROR: Sorry but this version of Hammr (version = 'HAMMR_VERSION') is not compatible with the version of UForge (version = 'UFORGE_VERSION').
	ERROR: Please refer to 'Install Compatibility' section in the documentation to learn how to install a compatible version of Hammr.


To install the correct version of Hammr, please run the command below indicating HAMMR-VERSION you want:

.. code-block:: shell
	
	$ pip install hammr==HAMMR-VERSION

