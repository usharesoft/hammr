# Copyright 2007-2015 UShareSoft SAS, All rights reserved
#
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from uforge.objects.uforge import *
from ussclicore.utils import printer



##--------------------- Cloud Formats

def generate_vcd(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    if "hwType" in builder["hardwareSettings"]:
        installProfile.hwType = builder["hardwareSettings"]["hwType"]
    image.compress = False
    return image, installProfile


def generate_nimbula(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    image.compress = True
    return image, installProfile


def generate_nimbulaesx(image, builder, installProfile, api, login):
    return generate_nimbula(image, builder, installProfile, api, login)


def generate_nimbulakvm(image, builder, installProfile, api, login):
    return generate_nimbula(image, builder, installProfile, api, login)


def generate_openstackqcow2(image, builder, installProfile, api, login):
    image.compress = False
    return image, installProfile


def generate_openstackvhd(image, builder, installProfile, api, login):
    image.compress = False
    return image, installProfile


def generate_openstackvmdk(image, builder, installProfile, api, login):
    image.compress = False
    return image, installProfile


def generate_openstackvdi(image, builder, installProfile, api, login):
    image.compress = False
    return image, installProfile


def generate_susecloud(image, builder, installProfile, api, login):
    image.compress = False
    return image, installProfile


def generate_eucalyptus(image, builder, installProfile, api, login):
    if not "account" in builder:
        printer.out("Account not found in builder", printer.ERROR)
        return None, None, None

    accounts = api.Users(login).Accounts.Getall()
    if accounts is None or not accounts.get_credAccount():
        printer.out("No accounts available", printer.ERROR)
        return None, None, None
    else:
        for account in accounts.get_credAccount():
            if account.name == builder["account"]["name"]:
                image.credAccount = account
                break

    if "disableRootLogin" in builder:
        myrootUser = osUser()
        if builder["disableRootLogin"] == "true":
            val = True
        elif builder["disableRootLogin"] == "false":
            val = False
        else:
            printer.out("Unknown value for 'disableRootLogin' in builder [ami]", printer.ERROR)
            return None, None, None
        myrootUser.disablePasswordLogin = val
        installProfile.rootUser = myrootUser

    image.compress = False
    return image, installProfile


def generate_eucalyptusxen(image, builder, installProfile, api, login):
    return generate_eucalyptus(image, builder, installProfile, api, login)


def generate_eucalyptuskvm(image, builder, installProfile, api, login):
    return generate_eucalyptus(image, builder, installProfile, api, login)


def generate_flexiant(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    # Compress is mandatory
    image.compress = True
    return image, installProfile


def generate_flexiantraw(image, builder, installProfile, api, login):
    return generate_flexiant(image, builder, installProfile, api, login)


def generate_flexiantova(image, builder, installProfile, api, login):
    return generate_flexiant(image, builder, installProfile, api, login)


def generate_flexiantkvm(image, builder, installProfile, api, login):
    return generate_flexiant(image, builder, installProfile, api, login)


def generate_cloudstackqcow2(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    image.compress = True
    return image, installProfile


def generate_cloudstackvhd(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    image.compress = True
    return image, installProfile


def generate_cloudstackova(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    image.compress = True
    return image, installProfile


def generate_abiquo(image, builder, installProfile, api, login):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    if "hwType" in builder["hardwareSettings"]:
        installProfile.hwType = builder["hardwareSettings"]["hwType"]
    image.compress = False
    return image, installProfile


def generate_azure(image, builder, installProfile, api, login):
    image.compress = False
    return image, installProfile


def generate_aws(image, builder, installProfile, api, login):
    image.ebs = True
    if "diskSize" in builder["installation"]:
        image.ebsVolumeSize = builder["installation"]["diskSize"]
    else:
        printer.out("No disksize set for ebs volume in builder [aws]", printer.ERROR)
        return None, None

    if "disableRootLogin" in builder:
        myrootUser = osUser()
        if builder["disableRootLogin"] == "true":
            val = True
        elif builder["disableRootLogin"] == "false":
            val = False
        else:
            printer.out("Unknown value for 'disableRootLogin' in builder [aws]", printer.ERROR)
            return None, None
        myrootUser.disablePasswordLogin = val
        installProfile.rootUser = myrootUser

    image.compress = False
    return image, installProfile


def generate_gce(image, builder, installProfile, api, login):
    image.compress = True
    return image, installProfile


def generate_outscale(image, builder, installProfile, api, login):
    image.compress = False
    return image, installProfile

def generate_k5vmdk(image, builder, installProfile, api, login):
    image.compress = False
    return image, installProfile

def generate_oracleraw(image, builder, installProfile, api, login):
    image.compress = True
    return image, installProfile

##--------------------- Physical Formats
def generate_iso(image, builder, installProfile, api=None, login=None):
    image.compress = True
    return image, installProfile

def generate_pxe(image, builder, installProfile, api=None, login=None):
    image.compress = False
    return image, installProfile


##--------------------- Virtual Formats    
def generate_ovf(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    if "hwType" in builder["hardwareSettings"]:
        installProfile.hwType = builder["hardwareSettings"]["hwType"]
    image.compress = True
    return image, installProfile


def generate_kvm(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    image.compress = True
    return image, installProfile


def generate_vbox(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    image.compress = True
    return image, installProfile


def generate_raw(image, builder, installProfile, api=None, login=None):
    image.compress = True
    return image, installProfile


def generate_hyper_v(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    image.compress = True
    return image, installProfile


def generate_qcow2(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    image.compress = True
    return image, installProfile


def generate_vhd(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    image.compress = True
    return image, installProfile


def generate_xen(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    image.compress = True
    return image, installProfile


def generate_vagrant(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None

    if "publicBaseBox" in builder and builder["publicBaseBox"] == "true":
        # private vagrant
        if not "osUser" in builder:
            printer.out("osUser not found in vagrant builder", printer.ERROR)
            return None, None, None
        if not "sshKey" in builder:
            printer.out("sshKey not found in vagrant builder", printer.ERROR)
            return None, None, None

        # create ssh key for the user
        sshkey = generics_utils.create_user_ssh_key(self.api, self.login, builder["sshKey"])
        if sshkey == 2:
            return None, None, None

        sshKeys = sshKeys()
        sshKeys.add_sshKey(sshkey)
        vagrantUser = osUser()
        vagrantUser.name = builder["osUser"]
        vagrantUser.sshKeys = sshKeys
        installProfile.osusers.add_osUser(vagrantUser)
    else:
        pass

    image.compress = True
    return image, installProfile


def generate_xenserver(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    image.compress = True
    return image, installProfile


def generate_vmware(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    if "hwType" in builder["hardwareSettings"]:
        installProfile.hwType = builder["hardwareSettings"]["hwType"]
    image.compress = True
    return image, installProfile


def generate_vcenter(image, builder, installProfile, api=None, login=None):
    installProfile = get_memory_amount(builder, installProfile, True)
    if installProfile == 2:
        return None, None, None
    if "hwType" in builder["hardwareSettings"]:
        installProfile.hwType = str(builder["hardwareSettings"]["hwType"])
    image.compress = False
    return image, installProfile


def generate_targz(image, builder, installProfile, api=None, login=None):
    image.compress = True
    return image, installProfile


##--------------------- Container Formats
def generate_lxc(image, builder, installProfile, api=None, login=None):
    image.compress = True
    return image, installProfile


def generate_docker(image, builder, installProfile, api=None, login=None):
    image.compress = True
    return image, installProfile


##--------------------- Utils
def get_memory_amount(builder, installProfile, is_mandatory):
    if "hardwareSettings" in builder and "memory" in builder["hardwareSettings"]:
        installProfile.memorySize = builder["hardwareSettings"]["memory"]
        return installProfile
    else:
        if is_mandatory:
            printer.out("Error: no hardwareSettings part for builder [" + builder["type"] + "]", printer.ERROR)
            return 2
        else:
            return installProfile


def get_target_format_object(api, login, targetFormatName):
    targetFormatsUser = api.Users(login).Targetformats.Getall()
    if targetFormatsUser is None or len(targetFormatsUser.targetFormats.targetFormat) == 0:
        return None
    else:
        for item in targetFormatsUser.targetFormats.targetFormat:
            if (item.name == targetFormatName):
                return item
    return None
