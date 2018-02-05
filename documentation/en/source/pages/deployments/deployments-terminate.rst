.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _deployments-terminate:

Terminating a deployment
========================

You terminate a deployment by running ``deploy terminate``:

.. code-block:: shell

	$ hammr deploy terminate --id <your-id>
        Do you really want to delete deployment with id t0id1exb3d [Y/n] 
        Y
        Deployment is stopping
        |##############################################################|
        OK: Deployment terminated


This command will delete your deployment on the targeted cloud. You cand find the ID of the deployment by using the command ``deploy list``.
