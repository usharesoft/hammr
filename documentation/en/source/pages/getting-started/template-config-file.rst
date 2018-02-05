.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _template-config-file:

Template Configuration File
---------------------------

All machine images are created from a JSON or YAML configuration file, known as the ``template``. Templates provide all the information (os packages, software files, configuration) to describe the machine image you wish to build. This template is used by hammr to create the template (in meta-data) into the UForge Server and build one or more identical machine images. These images can then be registered to the respective environment ready for provisioning. Once a template is created in the UForge Server, hammr can be used to track and apply package updates for the template. Hammr can also export a template registered in the UForge Server to an archive that includes all the software and the original template configuration file.

.. image:: /images/hammr-workflow.png
