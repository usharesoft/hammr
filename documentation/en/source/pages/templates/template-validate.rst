.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _template-validate:

Validating Your Template
========================

Once you have created and modified your template file, it is best practice to validate your template before you build or publish it. In order to check that your template does not have any syntax errors or missing mandatory values, run the command ``validate``.

.. code-block:: shell

	$ hammr template validate --file <path/filename>.json
	Validating the template file [/Users/james/nginx-template.json] ...
	OK: Syntax of template file [/Users/james/nginx-template.json] is ok

If there are any errors, this command will tell you.

