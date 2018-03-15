.. Copyright (c) 2007-2018 UShareSoft, All rights reserved

.. _pkg-what-dependencies:

What is a Dependency
====================

A dependency is a piece of information in a software package that describes which other packages it requires to function correctly. Many packages require operating system libraries as they provide common services that just about every program uses (filesystem, network, memory etc).

For example, network applications typically depend on lower-level networking libraries provided by the operating system. The principle behind package dependencies is to share software, allowing software developers to write and maintain less code at a higher quality. Operating systems have thousands of packages.

In the world of virtualization and cloud computing, it is becoming imperative to strip down the number of operating system packages to just the required packages to run a particular application. This process, known as JeOS (pronounced “juice”) standing for “Just Enough Operating System” is a very painful manual process. So much so that many operating system vendors now supply a core operating system ISO with the minimum set of packages required to boot the system. The fun then begins as you manually install only the packages (and their dependencies) required to run your application.

Calculating Package Dependencies
================================

Package dependency checking occurs when you build (or generate) a new machine image. During the first phase of generation, the backend UForge Server calculates automatically all the dependencies of each package in the os section (profile and pkgs list) as well as any packages contained elsewhere in your stack (native packages declared in one or more bundles).

All missing packages are automatically added. For each package added, this package’s dependencies are also checked. This process continues until all the dependencies have been met. The end result is a complete dependency tree of all the packages you require to run your application. All these packages are added to the machine image. Consequently you should not be surprised if the number of packages that are actually installed are larger than the packages listed in the stack section of the template.

Each package has meta-data on what the package requires (that is, what the package depends on) and what it provides in terms of functionality. This meta-data varies on the package type (RPM, DEB etc).

The dependency calculation is done using a specific moment in time. This date is determined by the ``updateTo`` key in your stack. If this key does not exist, then the date the template was created (via the command ``template create``) is used. Chosen package versions and dependencies are calculated by ensuring that they are equal to or less than this date. Let’s take an example. Imagine you create a new stack on June 17th 2013, 17:00 GMT+1, and you choose package A, B and C. Packages A, B and C may have more than one version (updates added to the repository due to bug fixing and or new features). The versions displayed for A, B and C will be dates of each of these packages closest (but inferior) to our date.

.. image:: /images/package-updates1.png
