.. Copyright (c) 2007-2019 UShareSoft, All rights reserved

.. _machine-image-download:

Downloading a Machine Image
===========================

Only compressed images and Docker based images can be downloaded.

In case of a compressed image, you will need the image ``Id`` number in order to download it as follows. You must also set the location where the image should be saved.  To download a machine image, use the command ``image download``.

.. code-block:: shell

    $ hammr image download -c ~/.hammr/credentials-UFOL.yml --id 17517 --file /tmp/test.tar,gz
    INFO: no username nor password provided on command line, trying credentials file
    INFO: Using credentials file: /home/joris/.hammr/credentials-UFOL.yml
    INFO: Using url https://uforge.usharesoft.com/api
    Searching image with id [17517] ...
    Status: 100% |>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>| Time: 0:01:11
    OK: Image downloaded

In case of a Docker based image, you will need the image ``Id`` number in order to retrieve the ``docker pull`` command through the ``image download`` command.

.. code-block:: shell

    $ hammr image download --id 130590
    OK: In order to download the image, please run:
    docker pull uforge.usharesoft.com/software/718/130590/32ee61a82362705babd8daf07cd509a4ca93f0e
