# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


from uforge.objects.xsd0 import *
import printer



VIRTUAL_FORMATS = {'vcenter': 'vcenter','vmware ': 'vmware','ovf': 'ovf', 'kvm': 'kvm', 'vbox': 'vbox', 'raw': 'raw', 'hyper-v': 'hyper-v', 'qcow2': 'qcow2', 'xen': 'xen', 'vhd': 'vhd', 'vagrant': 'vagrant', 'citrix-xen': 'xenserver',};
CLOUD_FORMATS = {'gce': 'google', 'vcd': 'vcloud', 'nimbula-esx': 'nimbulaesx', 'nimbula-kvm': 'nimbulakvm', 'susecloud': 'susecloud', 'openstack': 'openstack', 'eucalyptus-xen': 'emi-xen', 'eucalyptus-kvm': 'emi-kvm', 'flexiant-raw': 'flexiantraw', 'flexiant-ova': 'flexiantova', 'flexiant-kvm': 'flexiantkvm', 'cloudstack-qcow2': 'cloudcomqcow2', 'cloudstack-vhd': 'cloudcomvhd', 'cloudstack-ova': 'cloudcomova', 'abiquo': 'abiquo', 'azure': 'azure', 'ami': 'ami'};
PHYSICAL_FORMATS = {'iso': 'ISO'};


##--------------------- Cloud Formats

def generate_vcd(image, builder, installProfile, api, login):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        if "hwType" in builder["hardwareSettings"]:
                installProfile.hwType = builder["hardwareSettings"]["hwType"]
        image.compress=False
        myimageFormat = imageFormat(name=CLOUD_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile 
        
def generate_nimbula(image, builder, installProfile, api, login):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        image.compress=True
        myimageFormat = imageFormat(name=CLOUD_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_nimbula_esx(image, builder, installProfile, api, login):
        return generate_nimbula(image, builder, installProfile, api, login)
    
def generate_nimbula_kvm(image, builder, installProfile, api, login):
        return generate_nimbula(image, builder, installProfile, api, login)
    
def generate_openstack(image, builder, installProfile, api, login):
        image.compress=False
        myimageFormat = imageFormat(name=CLOUD_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_susecloud(image, builder, installProfile, api, login):
        image.compress=False
        myimageFormat = imageFormat(name=CLOUD_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_eucalyptus(image, builder, installProfile, api, login):
        if not "account" in builder:
                printer.out("Account not found in builder", printer.ERROR)
                return  None,None,None
            
        accounts = api.Users(login).Accounts.Getall()
        if accounts is None or not accounts.get_credAccount():
                printer.out("No accounts available", printer.ERROR)
                return None,None,None
        else:
                for account in accounts.get_credAccount():
                        if account.name == builder["account"]["name"]:
                                image.credAccount = account
                                break

        if "disableRootLogin" in builder:
                myrootUser = osUser()
                if builder["disableRootLogin"]=="true":
                        val=True
                elif builder["disableRootLogin"]=="false":
                        val=False
                else:
                        printer.out("Unknown value for 'disableRootLogin' in builder [ami]", printer.ERROR)
                        return None,None,None
                myrootUser.disablePasswordLogin = val
                installProfile.rootUser = myrootUser                        

        image.compress=False
        myimageFormat = imageFormat(name=CLOUD_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
 
                 
    
def generate_eucalyptus_xen(image, builder, installProfile, api, login):
        return generate_eucalyptus(image, builder, installProfile, api, login)            
    
def generate_eucalyptus_kvm(image, builder, installProfile, api, login):
        return generate_eucalyptus(image, builder, installProfile, api, login)
    
def generate_flexiant(image, builder, installProfile, api, login):
        installProfile = get_memory_amount(builder, installProfile, True)
        #Compress is mandatory
        image.compress=True
        myimageFormat = imageFormat(name=CLOUD_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile

def generate_flexiant_raw(image, builder, installProfile, api, login):
        return generate_flexiant(image, builder, installProfile, api, login)
    
def generate_flexiant_ova(image, builder, installProfile, api, login):
        return generate_flexiant(image, builder, installProfile, api, login)
    
def generate_flexiant_kvm(image, builder, installProfile, api, login):
        return generate_flexiant(image, builder, installProfile, api, login)

def generate_cloudstack_qcow2(image, builder, installProfile, api, login):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        image.compress=True
        myimageFormat = imageFormat(name=CLOUD_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile

def generate_cloudstack_vhd(image, builder, installProfile, api, login):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        image.compress=True
        myimageFormat = imageFormat(name=CLOUD_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_cloudstack_ova(image, builder, installProfile, api, login):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        image.compress=True
        myimageFormat = imageFormat(name=CLOUD_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_abiquo(image, builder, installProfile, api, login):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        if "hwType" in builder["hardwareSettings"]:
                installProfile.hwType = builder["hardwareSettings"]["hwType"]
        image.compress=False
        myimageFormat = imageFormat(name=CLOUD_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_azure(image, builder, installProfile, api, login):
        image.compress=False
        myimageFormat = imageFormat(name=CLOUD_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_ami(image, builder, installProfile, api, login):
        if not "account" in builder:
                printer.out("Account not found in builder", printer.ERROR)
                return None,None,None
        if not "name" in builder["account"]:
                printer.out("Account anme not found in builder", printer.ERROR)
                return None,None,None
        
        accounts = api.Users(login).Accounts.Getall()
        if accounts is None or not hasattr(accounts, 'get_credAccount'):
                printer.out("No accounts available", printer.ERROR)
                return None,None,None

        for account in accounts.get_credAccount():
                if account.name == builder["account"]["name"]:
                        image.credAccount = account
                        break
        if "disableRootLogin" in builder:
                myrootUser = osUser()
                if builder["disableRootLogin"]=="true":
                        val=True
                elif builder["disableRootLogin"]=="false":
                        val=False
                else:
                        printer.out("Unknown value for 'disableRootLogin' in builder [ami]", printer.ERROR)
                        return None,None,None
                myrootUser.disablePasswordLogin = val
                installProfile.rootUser = myrootUser
                
        if "updateAWSTools" in builder:
                image.update
                
        if "ebs" in builder:
                if "installation" in builder and "diskSize" in builder["installation"]:
                        installProfile.ebsVolumeSize = builder["installation"]["diskSize"]
                else:
                        printer.out("No disksize set for ebs volume in builder [ami]", printer.ERROR)
                        return None,None,None
                
    
        image.compress=False
        myimageFormat = imageFormat(name=CLOUD_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile

def generate_gce(image, builder, installProfile, api, login):
        image.compress=True
        myimageFormat = imageFormat(name=CLOUD_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
                

##--------------------- Physical Formats
def generate_iso(image, builder, installProfile):
        image.compress=True
        myimageFormat = imageFormat(name=PHYSICAL_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
    
##--------------------- Virtual Formats    
def generate_ovf(image, builder, installProfile):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        if "hwType" in builder["hardwareSettings"]:
                installProfile.hwType = builder["hardwareSettings"]["hwType"]
        image.compress=True
        myimageFormat = imageFormat(name=VIRTUAL_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile

def generate_kvm(image, builder, installProfile):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        image.compress=True
        myimageFormat = imageFormat(name=VIRTUAL_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_vbox(image, builder, installProfile):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        image.compress=True
        myimageFormat = imageFormat(name=VIRTUAL_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile

def generate_raw(image, builder, installProfile):
        image.compress=True
        myimageFormat = imageFormat(name=VIRTUAL_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_hyper_v(image, builder, installProfile):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        image.compress=True
        myimageFormat = imageFormat(name=VIRTUAL_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_qcow2(image, builder, installProfile):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        image.compress=True
        myimageFormat = imageFormat(name=VIRTUAL_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_vhd(image, builder, installProfile):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        image.compress=True
        myimageFormat = imageFormat(name=VIRTUAL_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile

def generate_xen(image, builder, installProfile):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        image.compress=True
        myimageFormat = imageFormat(name=VIRTUAL_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_vagrant(image, builder, installProfile):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        

        if "publicBaseBox" in builder and builder["publicBaseBox"]=="true":
                #private vagrant
                if not "osUser" in builder:
                        printer.out("osUser not found in vagrant builder", printer.ERROR)
                        return None,None,None
                if not "sshKey" in builder:
                        printer.out("sshKey not found in vagrant builder", printer.ERROR)
                        return None,None,None
                
                #create ssh key for the user
                sshkey = generics_utils.create_user_ssh_key(self.api, self.login, builder["sshKey"])
                if sshkey==2:
                        return None,None,None
                
                sshKeys = sshKeys()
                sshKeys.add_sshKey(sshkey)
                vagrantUser = osUser()
                vagrantUser.name = builder["osUser"]
                vagrantUser.sshKeys = sshKeys
                installProfile.osusers.add_osUser(vagrantUser)
        else:
                pass
         
        image.compress=True
        myimageFormat = imageFormat(name=VIRTUAL_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_citrix_xen(image, builder, installProfile):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        image.compress=True
        myimageFormat = imageFormat(name=VIRTUAL_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile
    
def generate_vmware(image, builder, installProfile):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        if "hwType" in builder["hardwareSettings"]:
                installProfile.hwType = builder["hardwareSettings"]["hwType"]
        image.compress=True
        myimageFormat = imageFormat(name=VIRTUAL_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile    
    
def generate_vcenter(image, builder, installProfile):
        installProfile = get_memory_amount(builder, installProfile, True)
        if installProfile==2:
                return None,None,None
        if "hwType" in builder["hardwareSettings"]:
                installProfile.hwType = builder["hardwareSettings"]["hwType"]
        image.compress=False
        myimageFormat = imageFormat(name=VIRTUAL_FORMATS[builder["type"]])
        return image,myimageFormat,installProfile 
    
    
    
##--------------------- Utils
def get_memory_amount(builder, installProfile, is_mandatory):
        if "hardwareSettings" in builder and "memory" in builder["hardwareSettings"]:
                installProfile.memorySize = builder["hardwareSettings"]["memory"]
                return installProfile
        else:
                if is_mandatory:
                        printer.out("Error: no hardwareSettings part for builder ["+builder["type"]+"]", printer.ERROR)
                        return 2
                else:
                        return installProfile
                    
def map_format(formatName):
        for mappedFormat in VIRTUAL_FORMATS:
                if VIRTUAL_FORMATS[mappedFormat]==formatName:
                        return mappedFormat
        for mappedFormat in CLOUD_FORMATS:
            if CLOUD_FORMATS[mappedFormat]==formatName:
                return mappedFormat
        for mappedFormat in PHYSICAL_FORMATS:
            if PHYSICAL_FORMATS[mappedFormat]==formatName:
                return mappedFormat