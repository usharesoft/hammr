.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _install-linux:

For Linux
=========

First of all, you need to install extra packages on your system

Debian based system:

.. code-block:: shell
	
	$ apt-get install python-dev gcc libxslt1-dev which

Red-hat based system:

.. code-block:: shell
	
	$ yum install gcc python-devel libxml2-devel libxslt-devel which redhat-rpm-config

Ubuntu system:

.. code-block:: shell
	
	$ sudo apt-get install libz-dev

Now, you are ready to install the latest version of Hammr:

.. code-block:: shell

	$ easy_install progressbar==2.3
	$ pip install hammr

If you want to install a specific version of Hammr, see :ref:`install-compatibility` to find the compatible version of UForge, and in the code above replace the ``pip install hammr`` with:

.. code-block:: shell

	$ pip install hammr==HAMMR-VERSION

If you already have hammr installed and want to upgrade to the latest version you can run:

.. code-block:: shell
	
	$ pip install --upgrade hammr

.. note:: You can only have one version of Hammr installed on your system.

.. note:: If you need to remove a version of hammr, you can will need to remove both ``hammr`` and the Python SDK.


