.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _authentication-methods:

Authentication
==============

Communication between hammr and the UForge server is done via HTTPS. To send requests to the UForge server, hammr needs the following information:

* UForge Server URL endpoint
* Your account user name
* Your password

This information can be passed to hammr either from command-line options or from a file.

Command-line Parameters
-----------------------

Authentication information can be passed to hammr via command-line options.  These options are:

* ``-a`` or ``--url``: the UForge Server URL endpoint.  If the URL uses HTTPS, then the connection will be done securely (recommended), otherwise connection will be done via HTTP
* ``-u`` or ``--user``: the user name to use for authentication
* ``-p`` or ``--password``: the password to use for authentication

For example

.. code-block:: shell

	$ hammr os list --url https://your-uforge.com/api -u username -p password

These parameters need to be passed each time you want to use the command-line.

Using Supervisor Mode
---------------------

UForge allows you to access UForge as another user if you have supervisor access. Supervisor access rights are assigned by the UForge administrator. 

.. warning:: Users with Supervisor Access will be able to log in as ANY of the users in the organization without entering a password. This right should be limited to support or managed services. Users with Supervisor Role needs to respect the privacy of the user data, according to current legislation.

To use hammr in supervisor mode you will need to enter your user name (UserA) as well as the user name of the account you want to access (UserB). For example:

.. code-block:: shell

	$ hammr os list --url https://uforge.usharesoft.com/api -u "UserA\UserB" -p password

Using a Credential File
=======================

Rather than passing the authentication information as part of the command-line, you can instead store this information in a credential file (``credentials.json`` or ``credentials.yml``) that will be used every time hammr is launched.  Hammr searches for this file in a sub-directory named ``.hammr`` located in the home directory of the user launching hammr.

For more information, refer to :ref:`credential-file`.