.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _pkg-dependencies:

Package Dependencies and Updates
================================

Hammr, via the build mechanism, determines the complete list of packages that must be installed by checking the dependencies of the packages you have listed in the ``os`` sub-section of the stack (via the profile and pkgs) and any native packages listed in a ``bundle``.  Hammr also provides a mechanism to track any available updates on these packages and allows you to update or roll-back your template.


.. toctree::
   :titlesonly:

   dependencies
   pkg-updates
   pkg-sticky