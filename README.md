Hammr
=====

A command-line tool for building consistent and repeatable machine images for different platforms.

Hammr supports the following platforms and machine image formats:

* Amazon EC2 (AMI) - EBS-backed and Ephemeral
* VMware : Desktop (Workstation, Fusion, Player); vSphere vCenter; vCloud Director
* Microsoft Azure
* Google Compute Engine
* Flexiant
* SuseCloud
* CloudStack
* OpenStack - para-virt and full-girt images
* Eucalyptus (EMI)
* Abiquo
* Nimbula
* Citrix Xen Server
* Hyper-V
* ISO
* KVM
* OVF
* QCOW2
* Raw
* Vagrant Base Box
* VirtualBox
* VHD
* Xen

Documentation
=============
Please visit:
* Website: [http://hammr.io](http://hammr.io)


Installation
============
Hammr is based on python, consequently it supports all major operating systems.  The easiest way to install hammr is using `pip`.

```$ pip install hammr
```

Installing From Source
======================
Firstly clone the repository to get all the source files.
Next go to the source directory where the `setup.py` file is located.
To compile and install, run (as sudo):
```$ sudo python setup.py build install`
```

This will automatically create the hammr executable and install it properly on your system.

To check that this was successful, run:

```$ hammr —-version` 
```

Upgrading
=========
If you have already installed hammr, and you with to upgrade to the latest version, use:
```$ pip install —upgrade hammr`
```


Feedback
========
If you have any questions or feedback, get in touch at [hammr@googlegroups.com](mailto:hammr%40googlegroups.com) or via: [Hammr Google Group](https://groups.google.com/d/forum/hammr)


License
=======
Hammr is licensed under the Apache 2.0 license. For more information, please refer to LICENSE file.
