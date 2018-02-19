.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _template-validate:

Validating Your Template
========================

Once you have created and modified your template file, it is best practice to validate your template before you build or publish it. In order to check that your template does not have any syntax errors or missing mandatory values, run the command ``validate``. The following example assumes you are using a YAML file but you can also use JSON.

.. code-block:: shell

	$ hammr template validate --file <path/filename>.yml
	Validating the template file [/Users/james/nginx-template.yml] ...
	OK: Syntax of template file [/Users/james/nginx-template.yml] is ok

If there are any errors, this command will tell you.

