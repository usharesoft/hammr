.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _builder-lxc:

LXC
====

Default builder type: ``LXC Container``

Require Cloud Account: No

`www.linuxcontainers.org <https://linuxcontainers.org/lxc/introduction/>`_

The LXC builder provides information for building a Linux container image.
This builder type is the default name provided by UForge AppCenter.

.. note:: This builder type name can be changed by your UForge administrator. To get the available builder type, please refer to :ref:`command-line-format`

The LXC builder section has the following definition when using YAML:

.. code-block:: yaml

  ---
  builders:
  - type: LXC Container
    # the rest of the definition goes here.

If you are using JSON:

.. code-block:: javascript

  {
    "builders": [
      {
        "type": "LXC Container",
        ...the rest of the definition goes here.
      }
    ]
  }

Building a Machine Image
------------------------

For building an image, the valid keys are:

* ``type`` (mandatory): a string providing the machine image type to build. Default builder type for LXC: ``LXC Container``. To get the available builder type, please refer to :ref:`command-line-format`.
