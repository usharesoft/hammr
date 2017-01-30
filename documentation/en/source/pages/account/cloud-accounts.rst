.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _cloud-accounts:

Setting Your Cloud Accounts
===========================

For security reasons, it is recommended not to add any cloud account information into the template file. Hammr allows you to register your cloud account information to the UForge server, then reference the cloud account tag name in the template.

To do this, you need to create a JSON file which contains all the necessary cloud credentials. This will depend on your cloud type. For more information, refer to the :ref:`template-builders` section of the documentation.

Once this file is ready, you create the cloud account on UForge by running the command ``account create``.

.. code-block:: shell

	$ hammr account create --file aws-account.json
	Validating the template file [aws-account.json] ...
	OK: Syntax of template file [aws-account.json] is ok
	Create account for 'ami'...
	OK: Account create successfully for [ami]

Once the cloud account is created, you can safely reference the cloud credentials in all the template files by using the account name.
