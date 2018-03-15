.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _install-windows:

For Windows
===========

For Windows users, first install Python 2.7, which can be found `here <https://www.python.org/downloads/>`_. Download the ``msi`` file, and install ``Python 2.7`` by executing the msi file. In the instructions below, we assume that the installation path for Python 2.7 is ``C:\Python27``.

Once Python 2.7 is installed, run the command for the latest version of Hammr:

.. code-block:: shell

	c:\Python27> .\Scripts\easy_install.exe hammr

If you want to install a specific version of Hammr, see :ref:`install-compatibility` to find the compatible version of UForge, and in the code above replace the '.\Scripts\easy_install.exe hammr' with:

.. code-block:: shell

	c:\Python27> .\Scripts\easy_install.exe hammr==HAMMR-VERSION

If your Windows does not have a compilation environment, ``pycrypto`` installation may fail.
You can install a ``pycrypto`` windows binary with this command (change your python version if needed):

.. code-block:: shell

	c:\Python27> .\Scripts\easy_install.exe http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe

If you already have hammr installed and want to upgrade to the latest version you can run:

.. code-block:: shell
	
	c:\Python27\Scripts> easy_install.exe --upgrade hammr

Add Python and hammr to system path:
Go to "My Computer > (right click) Properties > Advanced System Settings > Environment Variables"


You will get this configuration window:

.. image:: /images/install-windows.png

In ``System Variables``, search for the ``Path`` variable and click ``Edit``. Add the following at the end (replace ``C:\Python27`` with your Python installation path if it differs):

.. code-block:: shell

	;C:\Python27;C:\Python27\Scripts;


