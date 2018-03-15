.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _machine-image-download:

Downloading a Machine Image
===========================

You can only download images that have been compressed. You will need the image ``Id`` number in order to download it as follows. You must also set the location where the image should be saved.  To download a machine image, use the command ``image download``.

.. code-block:: shell

	$ hammr image download -c ~/.hammr/credentials-UFOL.yml --id 17517 --file /tmp/test.tar,gz
	INFO: no username nor password provided on command line, trying credentials file
	INFO: Using credentials file: /home/joris/.hammr/credentials-UFOL.yml
	INFO: Using url https://factory.usharesoft.com/api
	Searching image with id [17517] ...
	Status: 100% |>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>| Time: 0:01:11
	OK: Image downloaded

