.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

.. _template-builders:

Builders
========

Within a template, the ``builders`` section is an array of objects, describing the list of machine images to build (and where possible publish). For example if you wished to build an AMI image for Amazon EC2 and another for Microsoft Azure, you would specify a builder for each.

The information may include H/W requirements, authentication information (known as a cloud account) or where to upload and register the machine image after the build is complete.

Please refer to the specific machine image format for the mandatory and optional attributes.

.. rubric::  A Word on Cloud Accounts

For "cloud" machine images, for example Amazon EC2, Azure CloudStack, OpenStack, Flexiant and Eucalyptus, the ``builder`` requires account information to the cloud environment. Information from the builder is used to correctly generate the machine image (for example AMI images for Amazon EC2 requires to have certain certificates embedded into the machine image) and to upload and register the machine image into the correct region, zone or datacenter.

The cloud account information can be part of the builder section, however as this includes sensitive information, hammr provides other mechanisms to include this information in the builder section. A safer way is to store this information in a separate file (JSON or YAML) and create the cloud account using ``account create``; then reference the account ``name`` in the builder.

Please refer to the specific machine image format for the cloud account options and examples.

Cloud Targets
-------------

.. toctree::
   :titlesonly:

   builders-abiquo
   builders-aws
   builders-cloudstack
   builders-euca
   builders-flexiant
   builders-gce
   builders-azure
   builders-k5
   builders-nimbula
   builders-openstack
   builders-oracle-cloud
   builders-outscale
   builders-suse-cloud
   builders-vcd

Virtual Targets
---------------

.. toctree::
   :titlesonly:

   builders-citrix-xen
   builders-hyper-v
   builders-kvm
   builders-ovf
   builders-qcow2
   builders-raw
   builders-vagrant
   builders-vbox
   builders-vhd
   builders-vmware-workstation
   builders-vsphere
   builders-xen

Container Targets
-----------------

.. toctree::
   :titlesonly:

   builders-docker
   builders-lxc

Physical Targets
----------------

.. toctree::
   :titlesonly:

   builders-iso
   builders-pxe
