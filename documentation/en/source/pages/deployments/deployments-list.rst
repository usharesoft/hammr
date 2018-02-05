.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _deployments-list:

Listing the Deployments
=======================

You can check all your deployments by running ``deploy list``:

.. code-block:: shell

	$ hammr deploy list
	Getting all deployments for [root] ...
        Deployments:

        +--------------------+---------------+--------------+-----------+-------------+-----------+-------------+---------+----------------+
        |  Deployment name   | Deployment ID |   Hostname   | Region    | Source type | Source ID | Source Name | Status  | cloud provider |
        +====================+===============+==============+===========+=============+===========+=============+=========+================+
        | myscan-deploy      | i423btn74s    | 213.32.77.16 | eu-west-1 | Stack       | 104       | None        | running | openstack      |
        +--------------------+---------------+--------------+-----------+-------------+-----------+-------------+---------+----------------+
        | wordpress          | lcwuld9c07    | 213.32.73.26 | eu-west-1 | Scan        | 1         | None        | running | openstack      |
        +--------------------+---------------+--------------+-----------+-------------+-----------+-------------+---------+----------------+
        | myappliance-deploy | l6fl2swl5i    | None         | None      | None        | None      | None        | on-fire | aws            |
        +--------------------+---------------+--------------+-----------+-------------+-----------+-------------+---------+----------------+

        Found 3 deployments

The table lists the deployment ID, which you will need to terminate the instance, the hostname, region, source used and the status.
