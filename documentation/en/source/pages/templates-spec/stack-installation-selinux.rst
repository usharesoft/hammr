.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _stack-installation-selinux:

selinux
=======

The following is a list of all the accepted timezone values that can be used for the SELinux mode in an :ref:`stack-installation` sub-section of the stack.

For example:

.. code-block:: json

	{
	  "installation": {
	    "seLinuxMode" : "permissive"
	  }
	}

Available Keyboard Values
-------------------------

* ``disabled``
* ``permissive``
* ``enforcing``
