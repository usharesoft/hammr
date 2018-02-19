.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _install-mac:

For Mac
=======

For Mac users, you need to have ``XCode`` installed (or any other C compiler).

You can download the latest version of Xcode from the Apple developer website or get it using the Mac App Store

Run the following command to install the latest version of Hammr:

.. code-block:: shell

	$ xcode-select --install
	$ sudo easy_install pip
	$ sudo easy_install readline
	$ sudo easy_install progressbar==2.3
	$ sudo pip install hammr

If you want to install a specific version of Hammr, see :ref:`install-compatibility` to find the compatible version of UForge, and in the code above replace the 'sudo pip install hammr' with:

.. code-block:: shell

	$ sudo pip install hammr==HAMMR-VERSION

If you already have hammr installed and want to upgrade to the latest version you can run:

.. code-block:: shell

	$ pip install --upgrade hammr
