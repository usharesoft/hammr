.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _exporting-importing-templates:

Importing and Exporting
=======================

Hammr has a notion of importing and exporting templates. After creating a template from the JSON or YAML configuration file; this template can be exported as an archive. The archive will include the template file as well as any bundled software that was initially uploaded as part of the template creation.

The archive can then be used to import the template into another UForge Server instance.

The ``stack`` section of a template can include bundles of software and configuration information. This information may be stored locally on a filesystem or available via URLs. In some cases, when another user creates a template from the same template file (JSON or YAML), the custom software and/or configuration files may not be reachable or present. By creating an archive (using export) ensure that all relevant software for creating the template is available.



.. toctree::
   :titlesonly:

   export-template
   import-template