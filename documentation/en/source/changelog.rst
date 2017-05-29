.. Copyright (c) 2007-2016 UShareSoft, All rights reserved

Changelog
=========

hammr 3.7.4 (2017-28-04)
--------------------------

Evolutions:

* Compatibility with UForge AppCenter 3.7.fp4-1 only
* Add overlay argument to scan run command to run a scan with overlay

Bug fixes:

* Flag acceptAutoSigned not working for image download
* Name for the builder account can now be read from an external file
* Fixes on documentation

hammr 3.7.3 (2017-21-03)
--------------------------

Evolutions:

* Compatibility with UForge AppCenter 3.7.fp3-1 only

Bug fixes:

* Improve documentation for install compatibility between Hammr and UForge

hammr 3.7-3 (2017-16-02)
------------------------

Evolutions:

* Compatibility with UForge AppCenter 3.7-3 only
* Align bundle specification with UForge
* Support YAML files as input

Bug fixes:

* Improve documentation for install compatibility between Hammr and UForge

hammr 3.7.2-1 (2017-14-02)
--------------------------

Evolutions:

* Compatibility with UForge AppCenter 3.7.fp2-1 only
* Add Azure Resource Manager publish support
* Add Docker publish support
* Modify documentation for multi-nics option
* Align bundle specification with UForge
* Support YAML files as input

Bug fixes:

* Improve documentation for install compatibility between Hammr and UForge

hammr 3.7-2 (2017-31-01)
------------------------

Evolutions:

* Compatibility with UForge AppCenter 3.7-2 only
* Improve release process for Hammr
* Add Fujitsu K5 publish support
* Add release notes in documentation

Bug fixes:

* Fixes on documentation

hammr-3.6 1.1 (2016-16-12)
--------------------------

Evolutions:

* Improve project setup.py clean command
* Add travis CI build for the project
* Add an optional parameter to allow to change the ssh port used to connect on the running machine
* Ability to use a directory as source for bundle

Bug fixes:

* Scan build method generate exception
* Fix typo in os help message
* Some fixes on documentation
* A name including a space cannot be specified with hammr template clone
* Account list gives the class name instead of the account type
* The usage of the pkg parameter of hammr os search is not correct


hammr-3.6 0.1 (2016-07-01)
--------------------------

Evolutions:

* Compatibility with UForge AppCenter 3.6
	- Target formats and target platforms support
	- Builder part has been updated
* Hammr documentation now inside github repository
* Improve setup.py clean command
* Hammr uses a new download utility

Bug fixes:

* Ability to specify a timezone inside "updateTo" field for "stack"

Known issues:

* Amazon AWS format is not working
* Bootscript order is mandatory (incompatibility with Hammr on UForge AppCenter 3.5.1)
* Not possible to use both hammr 0.2.x and hammr-3.6 on the same system

0.2.5.10 (2016-04-29)
---------------------

Evolutions:

* Added hammr documentation to the github project
* Add support for uforge-python-sdk 3.5.1.4: ability to do streaming download

Bug fixes:

* ``hammr scan run`` fails when searching scan on uforge
* Using a relative path to the json file seems to invoke an error
* hammr image publish returns exception if there is no cloud account

0.2.5.9 (2015-12-18)
--------------------

Evolutions:

* Add compatibility with Outscale format

0.2.5.8 (2015-11-20)
--------------------

Evolutions:

* Increase timeout value

Bug fixes:

* Cannot install hammr because of a dependency error (issue #45)

0.2.5.7 (2015-09-21)
--------------------

Evolutions:

* Reuse existing bundles option while importing templates (issue #26)
* Template export directory clean up (issue #43)


0.2.5.6 (2015-08-29)
--------------------

Bug fixes:

* Fix issue #38 - Could be nice to have a way to specify credentials file from command line
* Fix issue #31 - "hammr scan delete" deletes every scan if scan id and scan instance id is the same.


0.2.5.5 (2015-08-04)
--------------------

Evolutions:

* Add support for lxc and targz for Hammr

Bug fixes:

* Fix issue #34 - Exit status of Hammr command
* Enhance the error message if an issue occurs when trying to download a machine image

