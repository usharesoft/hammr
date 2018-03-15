.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _installation:

Installation
============

To use hammr, you require to install it on the machine you wish to run it. Hammr is based on python, and is supported all major operating systems. The easiest way to install hammr is using ``pip`` the widely used package management system for installing and managing software packages written in python.

Installing pip
--------------

If you already have pip installed on your system, you can skip this step.

To install or upgrade pip, download `get-pip.py <https://bootstrap.pypa.io/get-pip.py>`_

Now run the command:

.. code-block:: shell

	$ python get-pip.py

For more information on installing pip, please refer to the official pip documentation:
`http://www.pip-installer.org/en/latest/installing.html <http://www.pip-installer.org/en/latest/installing.html>`_

Installing Hammr
----------------

Once pip has been installed, you can now install the hammr packages (note, you may have to run this command as ``sudo`` or ``administrator``).

.. note:: A version of Hammr is compatible with only one version of UForge. To see the compatibility table, go to :ref:`install-compatibility` section.

.. note:: You can only have one version of Hammr installedon your system.

Please refer to the installation instructions depending upon your desktop type:

.. toctree::
   :titlesonly:

   install-linux
   install-mac
   install-windows
   install-source
   install-verify
   install-compatibility
