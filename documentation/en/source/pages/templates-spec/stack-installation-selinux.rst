.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _stack-installation-selinux:

selinux
=======

The following is a list of all the accepted values that can be used for the SELinux mode in an :ref:`stack-installation` sub-section of the stack.

For example:

.. code-block:: json

	{
	  "installation": {
	    "seLinuxMode" : "permissive"
	  }
	}

Accepted Values
---------------

* ``disabled``
* ``permissive``
* ``enforcing``
