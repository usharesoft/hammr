.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _create-template-steps:

Creating Your First Machine Image
=================================

Now that hammr is installed, lets build our first machine image. Hammr can be used to build machine images containing pretty much any software for many different environments – from a trusty ISO image for physical machine deployments; to virtual and cloud environments.

In this example we are going to create a nginx machine image for Amazon EC2 based on Ubuntu 12.04 (64 bit).

.. note:: To go through this tutorial, you are going to need an AWS account. If you don’t have one, create a free account `here <http://aws.amazon.com/free/>`_. If you do not wish to create an AWS account, then you can still follow the tutorial, as creating machine images for other environments follows the same basic principles.

There are three phases when creating your machine image:

	* Defining the contents of the machine image in a template configuration file
	* Generating the machine image from the template to the required environment, in our case Amazon EC2.
	* Publishing and registering the image in AWS, ready to provision one or more machine instances from the machine image

The rest of this section highlights these steps to create your first machine image.

.. toctree::
   :titlesonly:

   create-template
   build-machine-image
   publish-machine-image
   next-steps
