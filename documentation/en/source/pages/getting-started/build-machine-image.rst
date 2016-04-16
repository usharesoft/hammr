.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _build-machine-image:

Building a Machine Image
========================

Once a template has been created, you can create a machine image from it. You can build as many machine images as you like for different platforms and environments. The result will be near identical machine images every time you build from the template. There will be minor differences depending upon the target platform. For example, building an Amazon EC2 image will automatically include the mandatory Amazon libraries required by EC2 to correctly provision an instance, while for OpenStack or VMware vCloud Director, these libraries are not required.

To build a machine image, you need to add the ``builders`` section to your file. The ``builder`` section provides mandatory parameters to build (and for some environments register) the machine image. Each target environment requires different ``builders`` parameters. Refer to the documentation for more information.

For security reasons, it is recommended not to add any cloud account information into the template file. Hammr provides various mechanisms to provide this cloud account information. The method we will use in this tutorial will be to register the cloud account information to the UForge server, then reference the cloud account tag name in the template. So create a file ``aws-account.json`` and add the following content:

.. code-block:: json

  {
    "accounts": [
      {
        "type": "ami",
        "name": "My AWS Account",
        "accountNumber": "111122223333",
        "x509PrivateKey": "/home/joris/accounts/aws/pk509.pem",
        "x509Cert": "/home/joris/accounts/aws/cert509.pem",
        "accessKey": "AAAABBBBCCCCDDDDEEEE",
        "secretAccessKey": "aaaa1111bbbb2222cccc3333dddd4444eeee5555"
      }
    ]
  }


To create the cloud account, use the command ``account create``

.. code-block:: shell

  $ hammr account create --file aws-account.json
  Validating the template file [aws-account.json] ...
  OK: Syntax of template file [aws-account.json] is ok
  Create account for 'ami'...
  OK: Account create successfully for [ami]

Once the cloud account is created, we can safely reference the cloud credentials in all the template files by using the account name, in this example: ``James AWS Account``

Lets now use this account to build a machine image for Amazon EC2. Open up the file ``nginx-template.json``, and provide the following content:

.. code-block:: json

  {
    "stack": {
      "name": "nginx",
      "version": "1.0",
      "os": {
        "name": "Ubuntu",
        "version": "12.04",
        "arch": "x86_64",
        "profile": "Minimal",
        "pkgs": [
          {
            "name": "iotop"
          }
        ]
      },
      "installation": {
        "diskSize": 12288
      }
    },
    "builders": [
      {
        "type": "ami",
        "account": {
          "name": "My AWS Account"
        },
        "installation": {
          "diskSize": 10240
        },
        "region": "eu-west-1",
        "s3bucket": "mybucketname"
      }
    ]
  }

You will notice that the new ``builders`` section includes the ``account`` name created earlier as well as the ``region`` and ``bucket`` where you will register the machine image.

To build the machine image, use the command ``template build``.

.. code-block:: shell

  $ hammr template build --file nginx-template.json
  Validating the template file [nginx-template.json] ...
  OK: Syntax of template file [nginx-template.json] is ok
  Generating 'ami' image (1/1)
  |>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>| 100%: Done, created on ... |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<|
  OK: Generation 'ami' ok
  Image URI: users/root/appliances/21/images/47
  Image Id : 47

