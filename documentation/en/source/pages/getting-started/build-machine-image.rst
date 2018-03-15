.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _build-machine-image:

Building a Machine Image
========================

Once a template has been created, you can create a machine image from it. You can build as many machine images as you like for different platforms and environments. The result will be near identical machine images every time you build from the template. There will be minor differences depending upon the target platform. For example, building an Amazon EC2 image will automatically include the mandatory Amazon libraries required by EC2 to correctly provision an instance, while for OpenStack or VMware vCloud Director, these libraries are not required.

To build a machine image, you need to add the ``builders`` section to your file. The ``builder`` section provides mandatory parameters to build (and for some environments register) the machine image. Each target environment requires different ``builders`` parameters. Refer to the documentation for more information.

For security reasons, it is recommended not to add any cloud account information into the template file. Hammr provides various mechanisms to provide this cloud account information. The method we will use in this tutorial will be to register the cloud account information to the UForge server, then reference the cloud account tag name in the template. So create a file ``aws-account.yml`` (or ``aws-account.json`` if you are using JSON) and add the following content:

.. code-block:: yaml

  ---
  accounts:
  - type: Amazon
    name: James AWS Account
    accountNumber: 11111-111111-1111
    accessKeyId: myaccessKeyid
    secretAccessKeyId: mysecretaccesskeyid
    x509Cert: "/home/developer/UShareSoft/WKS/Hammr/tests/certs/aws/aws.cert.pem"
    x509PrivateKey: "/home/developer/UShareSoft/WKS/Hammr/tests/certs/aws/aws.key.pem"

If you are using JSON:

.. code-block:: json

  {
    "accounts": [
      {
        "type": "Amazon",
        "name": "James AWS Account",
        "accountNumber": "11111-111111-1111",
        "accessKeyId": "myaccessKeyid",
        "secretAccessKeyId": "mysecretaccesskeyid",
        "x509Cert": "/home/developer/UShareSoft/WKS/Hammr/tests/certs/aws/aws.cert.pem",
        "x509PrivateKey": "/home/developer/UShareSoft/WKS/Hammr/tests/certs/aws/aws.key.pem"
      }
    ]
  }


To create the cloud account, use the command ``account create``, where ``--file`` is the YAML or JSON file you created.

.. code-block:: shell

  $ hammr account create --file aws-account.yml
  Validating the template file [aws-account.yml] ...
  OK: Syntax of template file [aws-account.yml] is ok
  Create account for 'ami'...
  OK: Account create successfully for [ami]

Once the cloud account is created, we can safely reference the cloud credentials in all the template files by using the account name, in this example: ``James AWS Account``

Lets now use this account to build a machine image for Amazon EC2. Open up the file ``nginx-template.yml``, and provide the following content:

.. code-block:: yaml

  ---
  stack:
    name: nginx
    version: '1.0'
    os:
      name: Ubuntu
      version: '12.04'
      arch: x86_64
      profile: Minimal
      pkgs:
      - name: iotop
    installation:
      diskSize: 12288
  builders:
  - type: Amazon
    account:
      name: James AWS Account
    installation:
      diskSize: 10240
    region: eu-west-1
    s3bucket: mybucketname

If you are using JSON (file ``nginx-template.json``):

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
        "type": "Amazon",
        "account": {
          "name": "James AWS Account"
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

  $ hammr template build --file nginx-template.yml
  Validating the template file [nginx-template.yml] ...
  OK: Syntax of template file [nginx-template.yml] is ok
  Generating 'ami' image (1/1)
  |>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>| 100%: Done, created on ... |<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<|
  OK: Generation 'ami' ok
  Image URI: users/root/appliances/21/images/47
  Image Id : 47

