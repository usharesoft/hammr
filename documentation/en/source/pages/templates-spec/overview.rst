.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _templates-spec:

Templates Specification
=======================

Templates contain all the information used to create stacks; build machine images and publish them to the target platform. They are JSON or YAML files, passed as a parameter to the hammr command-line.

A template has two main parts:

* ``stack``: defines the packages, files and configuration scripts of the machine image to build.
* ``builders``: an array defining the format of the machine images to build.

.. toctree::
   :titlesonly:

   stack
   builders/overview