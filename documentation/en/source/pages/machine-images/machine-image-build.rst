.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _machine-image-build:

Building a Machine Image
========================

In order to generate a machine image based on the template you created, you must update the template with the information for each type of image you want to generate (physical, virtual or cloud). This is done in the ``builders`` section of the configuration file.

The parameters you need to enter will depend on the type of image you want to generate. For a complete list of the mandatory and optional fields, see the builders list. Note that you can define several types of images in the same template.

When you run the hammr command to generate the images, all image formats defined in the builders section will be built at the same time.

Once the template is updated, build the images by running the command ``template build``. The file specified in ``--file`` can either be a JSON or YAML file.

.. code-block:: shell

	$ hammr template build --file <path/filename>.yml
	Validating the template file [nginx-template.yml] ...
	OK: Syntax of template file [nginx-template.yml] is ok
	Generating 'ami' image (1/1)
	|>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>| 100%: Done, created on ... |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<|
	OK: Generation 'ami' ok
	Image URI: users/root/appliances/21/images/47
	Image Id : 47

.. note:: This may take some time. A progress report is shown.