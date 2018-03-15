.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _install-source:

From Source
===========

Hammr has a dependency to ``uforge_python_sdk``. First, you need to install it:

.. code-block:: shell

	$ pip install uforge_python_sdk

or download sources from pypi: `https://pypi.python.org/pypi/uforge_python_sdk <https://pypi.python.org/pypi/uforge_python_sdk>`_

Go to the source directory where the ``setup.py`` file is located.
To compile and install, run (as sudo):

.. code-block:: shell

	$ python setup.py build; sudo python setup.py install

Now clone the Hammr git repository to get all the source files. Next go to the source directory where the ``setup.py`` file is located. To compile and install, run (as sudo):

.. code-block:: shell

	$ python setup.py build; sudo python setup.py install

This will automatically create the hammr executable and install it properly on your system.