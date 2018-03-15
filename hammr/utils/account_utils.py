# Copyright (c) 2007-2018 UShareSoft, All rights reserved
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

import ntpath

from uforge.objects.uforge import *
from ussclicore.utils import generics_utils, printer
from pyxb.utils import domutils


def openstack(account):
    myCredAccount = CredAccountOpenStack()
    # doing field verification
    if not "name" in account:
        printer.out("name for openstack account not found", printer.ERROR)
        return
    if not "glanceUrl" in account:
        printer.out("glanceUrl for openstack account not found", printer.ERROR)
        return
    if not "keystoneUrl" in account:
        printer.out("KeystoneUrl for openstack account not found", printer.ERROR)
        return
    if not "keystoneVersion" in account:
        printer.out("keystoneVersion for openstack account not found", printer.ERROR)
        return
    if not "login" in account:
        printer.out("login in openstack account not found", printer.ERROR)
        return
    if not "password" in account:
        printer.out("password in openstack account not found", printer.ERROR)
        return

    myCredAccount.name = account["name"]
    myCredAccount.glanceUrl = account["glanceUrl"]
    myCredAccount.keystoneUrl = account["keystoneUrl"]
    myCredAccount.keystoneVersion = account["keystoneVersion"]
    myCredAccount.login = account["login"]
    myCredAccount.password = account["password"]
    return myCredAccount


def susecloud(account):
    myCredAccount = SuseCloud()
    # doing field verification
    if not "username" in account:
        printer.out("username in susecloud account not found", printer.ERROR)
        return
    if not "password" in account:
        printer.out("catalogName in susecloud account not found", printer.ERROR)
        return
    if not "endpoint" in account:
        printer.out("endpoint for susecloud account not found", printer.ERROR)
        return
    if not "keystoneEndpoint" in account:
        printer.out("keystoneEndpoint for susecloud account not found", printer.ERROR)
        return
    if not "name" in account:
        printer.out("name for susecloud account not found", printer.ERROR)
        return

    myCredAccount.login = account["username"]
    myCredAccount.password = account["password"]
    myCredAccount.serverUrl = account["endpoint"]
    myCredAccount.keystoneUrl = account["keystoneEndpoint"]
    myCredAccount.name = account["name"]
    return myCredAccount


def cloudstack(account):
    myCredAccount = CredAccountCloudStack()
    # doing field verification
    if not "name" in account:
        printer.out("name for cloudstack account not found", printer.ERROR)
        return
    if not "publicApiKey" in account:
        printer.out("publicApiKey in cloudstack account not found", printer.ERROR)
        return
    if not "secretApiKey" in account:
        printer.out("secretApiKey in cloudstack account not found", printer.ERROR)
        return
    if not "endpointUrl" in account:
        printer.out("endpointUrl for cloudstack account not found", printer.ERROR)
        return

    myCredAccount.name = account["name"]
    myCredAccount.publicApiKey = account["publicApiKey"]
    myCredAccount.secretApiKey = account["secretApiKey"]
    myCredAccount.endpointUrl = account["endpointUrl"]
    return myCredAccount


def aws(account):
    myCredAccount = CredAccountAws()
    # doing field verification
    if not "accountNumber" in account:
        printer.out("accountNumber for ami account not found", printer.ERROR)
        return
    if not "name" in account:
        printer.out("name for ami account not found", printer.ERROR)
        return
    if not "accessKeyId" in account:
        printer.out("accessKey in ami account not found", printer.ERROR)
        return
    if not "secretAccessKeyId" in account:
        printer.out("secretAccessKey in ami account not found", printer.ERROR)
        return
    if not "x509Cert" in account:
        printer.out("x509Cert in ami account not found", printer.ERROR)
        return
    if not "x509PrivateKey" in account:
        printer.out("x509PrivateKey in ami account not found", printer.ERROR)
        return

    myCredAccount.accountNumber = account["accountNumber"]
    myCredAccount.name = account["name"]
    myCredAccount.accessKeyId = account["accessKeyId"]
    myCredAccount.secretAccessKeyId = account["secretAccessKeyId"]

    myCredAccount.certificates = pyxb.BIND()
    # A hack to avoid a toDOM, toXML bug
    myCredAccount.certificates._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Certificates')

    try:
        cert = certificate()
        with open(account["x509Cert"], "r") as myfile:
            cert.content_ = myfile.read()
        cert.type = "x509"
        cert.type._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'string')
        cert.name = ntpath.basename(account["x509Cert"])
        myCredAccount.certificates.append(cert)

        cert = certificate()
        with open(account["x509PrivateKey"], "r") as myfile:
            cert.content_ = myfile.read()
        cert.type = "ec2PrivateKey"
        cert.type._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'string')
        cert.name = ntpath.basename(account["x509PrivateKey"])
        myCredAccount.certificates.append(cert)

    except IOError as e:
        printer.out("File error: " + str(e), printer.ERROR)
        return

    return myCredAccount


def azure(account):
    if "publishsettings" in account:
        printer.out("Azure classic account")
        return azure_classic(account)
    else:
        printer.out("Azure Resource Manager account")
        return azure_arm(account)


def azure_arm(account):
    myCredAccount = CredAccountAzureResourceManager()
    # doing field verification
    if not "name" in account:
        printer.out("name for azure account not found", printer.ERROR)
        return
    if not "tenantId" in account:
        printer.out("no tenant id found", printer.ERROR)
        return
    if not "subscriptionId" in account:
        printer.out("no subscription id found", printer.ERROR)
        return
    if not "applicationId" in account:
        printer.out("no application id found", printer.ERROR)
        return
    if not "applicationKey" in account:
        printer.out("no application key found", printer.ERROR)
        return

    myCredAccount.name = account["name"]
    myCredAccount.tenantId = account["tenantId"]
    myCredAccount.subscriptionId = account["subscriptionId"]
    myCredAccount.applicationId = account["applicationId"]
    myCredAccount.applicationKey = account["applicationKey"]

    return myCredAccount


def azure_classic(account):
    myCredAccount = CredAccountAzure()
    # doing field verification
    if not "name" in account:
        printer.out("name for azure account not found", printer.ERROR)
        return
    if not "publishsettings" in account:
        printer.out("publishsettings in azure account not found", printer.ERROR)
        return

    myCredAccount.name = account["name"]
    myCredAccount.publishsettings = account["publishsettings"]

    myCredAccount.certificates = pyxb.BIND()
    # A hack to avoid a toDOM, toXML bug
    myCredAccount.certificates._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Certificates')

    try:
        cert = certificate()
        with open(account["publishsettings"], "r") as myfile:
            cert.content_ = myfile.read()
        cert.type = "azurePublishSettings"
        cert.type._ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'string')
        cert.name = ntpath.basename(account["publishsettings"])
        myCredAccount.certificates.append(cert)

    except IOError as e:
        printer.out("File error: " + str(e), printer.ERROR)
        return

    return myCredAccount


def eucalyptus(account):
    myCredAccount = CredAccountEws()
    # doing field verification
    if not "secretKey" in account:
        printer.out("secretKey in eucalyptus account not found", printer.ERROR)
        return
    if not "queryId" in account:
        printer.out("queryId in eucalyptus account not found", printer.ERROR)
        return
    if not "endpoint" in account:
        printer.out("endpoint in eucalyptus account not found", printer.ERROR)
        return
    if not "cloudCert" in account:
        printer.out("cloudCert in eucalyptus account not found", printer.ERROR)
        return
    if not "x509Cert" in account:
        printer.out("x509Cert in eucalyptus account not found", printer.ERROR)
        return
    if not "x509PrivateKey" in account:
        printer.out("x509PrivateKey in azure eucalyptus not found", printer.ERROR)
        return
    if not "accountNumber" in account:
        printer.out("accountNumber for eucalyptus account not found", printer.ERROR)
        return
    if not "name" in account:
        printer.out("name for eucalyptus account not found", printer.ERROR)
        return

    myCredAccount.accountNumber = account["accountNumber"]
    myCredAccount.name = account["name"]
    myCredAccount.hostname = account["endpoint"]
    myCredAccount.secretAccessKeyID = account["secretKey"]
    myCredAccount.accessKeyID = account["queryId"]

    myCertificates = certificates()
    myCredAccount.certificates = myCertificates

    try:
        myCertificate = certificate()
        with open(account["x509Cert"], "r") as myfile:
            myCertificate.certStr = myfile.read()
        myCertificate.type_ = "x509"
        myCertificate.name = ntpath.basename(account["x509Cert"])
        myCertificates.add_certificate(myCertificate)
        myCertificate = certificate()
        with open(account["x509PrivateKey"], "r") as myfile:
            myCertificate.certStr = myfile.read()
        myCertificate.type_ = "ec2PrivateKey"
        myCertificate.name = ntpath.basename(account["x509PrivateKey"])
        myCertificates.add_certificate(myCertificate)
        myCertificate = certificate()
        with open(account["cloudCert"], "r") as myfile:
            myCertificate.certStr = myfile.read()
        myCertificate.type_ = "eucCert"
        myCertificate.name = ntpath.basename(account["cloudCert"])
        myCertificates.add_certificate(myCertificate)


    except IOError as e:
        printer.out("File error: " + str(e), printer.ERROR)
        return

    return myCredAccount


def abiquo(account):
    myCredAccount = CredAccountAbiquo()
    # doing field verification
    if not "password" in account:
        printer.out("password in abiquo account not found", printer.ERROR)
        return
    if not "username" in account:
        printer.out("username in abiquo account not found", printer.ERROR)
        return
    if not "hostname" in account:
        printer.out("hostname for abiquo account not found", printer.ERROR)
        return
    if not "name" in account:
        printer.out("name for abiquo account not found", printer.ERROR)
        return

    myCredAccount.login = account["username"]
    myCredAccount.password = account["password"]
    myCredAccount.hostname = account["hostname"]
    myCredAccount.name = account["name"]
    return myCredAccount


def nimbula(account):
    myCredAccount = CredAccountNimbula()
    # doing field verification
    if not "password" in account:
        printer.out("password in nimbula account not found", printer.ERROR)
        return
    if not "username" in account:
        printer.out("username in nimbula account not found", printer.ERROR)
        return
    if not "endpoint" in account:
        printer.out("endpoint for nimbula account not found", printer.ERROR)
        return
    if not "name" in account:
        printer.out("name for nimbula account not found", printer.ERROR)
        return

    myCredAccount.login = account["username"]
    myCredAccount.password = account["password"]
    myCredAccount.serverUrl = account["endpoint"]
    myCredAccount.name = account["name"]
    return myCredAccount


def flexiant(account):
    myCredAccount = CredAccountFlexiant()
    # doing field verification
    if not "apiUsername" in account:
        printer.out("apiUsername in flexiant account not found", printer.ERROR)
        return
    if not "password" in account:
        printer.out("password in flexiant account not found", printer.ERROR)
        return
    if not "wsdlUrl" in account:
        printer.out("wsdlURL for flexiant account not found", printer.ERROR)
        return
    if not "name" in account:
        printer.out("name for flexiant account not found", printer.ERROR)
        return

    myCredAccount.apiUsername = account["apiUsername"]
    myCredAccount.password = account["password"]
    myCredAccount.wsdlUrl = account["wsdlUrl"]
    myCredAccount.name = account["name"]

    try:
        myCredAccount.userUUID = (myCredAccount.apiUsername).split('/')[1]
    except:
        printer.out(account["apiUsername"] + " is not a valid Flexiant username", printer.ERROR)
        return

    return myCredAccount


def vclouddirector(account):
    myCredAccount = CredAccountVCloudDirector()
    # doing field verification
    if not "name" in account:
        printer.out("name in vcd account not found", printer.ERROR)
        return
    if not "hostname" in account:
        printer.out("hostname in vcd account not found", printer.ERROR)
        return
    if not "login" in account:
        printer.out("login in vcd account not found", printer.ERROR)
        return
    if not "password" in account:
        printer.out("password in vcd account not found", printer.ERROR)
        return
    if not "organizationName" in account:
        printer.out("organizationName in vcd account not found", printer.ERROR)
        return

    if "port" in account:
        port = int(account["port"])
    else:
        port = 443

    myCredAccount.name = account["name"]
    myCredAccount.hostname = account["hostname"]
    myCredAccount.login = account["login"]
    myCredAccount.password = account["password"]
    myCredAccount.organizationName = account["organizationName"]
    myCredAccount.port = port

    return myCredAccount


def vsphere(account):
    myCredAccount = CredAccountVSphere()
    # doing field verification
    if not "name" in account:
        printer.out("name in vcenter account not found", printer.ERROR)
        return
    if not "login" in account:
        printer.out("login in vcenter account not found", printer.ERROR)
        return
    if not "password" in account:
        printer.out("password in vcenter account not found", printer.ERROR)
        return
    if not "hostname" in account:
        printer.out("hostname in vcenter account not found", printer.ERROR)
        return
    if "proxyHostname" in account:
        myCredAccount.proxyHost = account["proxyHostname"]
    if "proxyPort" in account:
        myCredAccount.proxyPort = account["proxyPort"]
    if "port" in account:
        port = int(account["port"])
    else:
        port = 443

    myCredAccount.name = account["name"]
    myCredAccount.login = account["login"]
    myCredAccount.password = account["password"]
    myCredAccount.hostname = account["hostname"]
    myCredAccount.port = port
    return myCredAccount


def gce(account):
    myCredAccount = CredAccountGoogle()
    # doing field verification
    if not "username" in account:
        printer.out("username in gce account not found", printer.ERROR)
        return
    if not "certPassword" in account:
        printer.out("certPassword in gce account not found", printer.ERROR)
        return
    if not "cert" in account:
        printer.out("cert in gce account not found", printer.ERROR)
        return
    if not "name" in account:
        printer.out("name for gce account not found", printer.ERROR)
        return

    myCredAccount.type_ = "google"
    myCredAccount.login = account["username"]
    myCredAccount.password = account["certPassword"]
    myCredAccount.name = account["name"]

    myCertificates = certificates()
    myCredAccount.certificates = myCertificates

    try:
        myCertificate = certificate()
        with open(account["cert"], "r") as myfile:
            myCertificate.certStr = myfile.read()
        myCertificate.type_ = "googleCertificate"
        myCertificate.name = ntpath.basename(account["cert"])
        myCertificates.add_certificate(myCertificate)

    except IOError as e:
        printer.out("File error: " + str(e), printer.ERROR)
        return

    return myCredAccount


def outscale(account):
    myCredAccount = CredAccountOutscale()
    # doing field verification
    if not "name" in account:
        printer.out("name for outscale account not found", printer.ERROR)
        return
    if not "accessKey" in account:
        printer.out("accessKey in outscale account not found", printer.ERROR)
        return
    if not "secretAccessKey" in account:
        printer.out("secretAccessKey in outscale account not found", printer.ERROR)
        return

    myCredAccount.secretAccessKeyID = account["secretAccessKey"]
    myCredAccount.accessKeyID = account["accessKey"]
    myCredAccount.name = account["name"]
    return myCredAccount

def k5(account):
    myCredAccount = CredAccountK5()
    # doing field verification
    if not "name" in account:
        printer.out("name for K5 account not found", printer.ERROR)
        return
    if not "login" in account:
        printer.out("login in K5 account not found", printer.ERROR)
        return
    if not "password" in account:
        printer.out("password in K5 account not found", printer.ERROR)
        return

    myCredAccount.name = account["name"]
    myCredAccount.login = account["login"]
    myCredAccount.password = account["password"]
    return myCredAccount

def docker(account):
    myCredAccount = CredAccountDocker()

    if not "name" in account:
        printer.out("name for Docker account is missing", printer.ERROR)
        return
    if not "endpointUrl" in account:
        printer.out("endpointUrl for Docker account is missing", printer.ERROR)
        return
    if not "login" in account:
        printer.out("login for Docker account is missing", printer.ERROR)
        return
    if not "password" in account:
        printer.out("password for Docker account is missing", printer.ERROR)
        return

    myCredAccount.name = account["name"]
    myCredAccount.endpointUrl = account["endpointUrl"]
    myCredAccount.login = account["login"]
    myCredAccount.password = account["password"]
    return myCredAccount

def oracle(account):
    myCredAccount = CredAccountOracle()

    if not "name" in account:
        printer.out("name for Oracle account is missing", printer.ERROR)
        return
    if not "login" in account:
        printer.out("login for Oracle account is missing", printer.ERROR)
        return
    if not "password" in account:
        printer.out("password for Oracle account is missing", printer.ERROR)
        return
    if not "domainName" in account:
        printer.out("domain name for Oracle account is missing", printer.ERROR)
        return

    myCredAccount.name = account["name"]
    myCredAccount.domainName = account["domainName"]
    myCredAccount.login = account["login"]
    myCredAccount.password = account["password"]
    return myCredAccount


def get_target_platform_object(api, login, targetPlatformName):
    targetPlatformsUser = api.Users(login).Targetplatforms.Getall()
    if targetPlatformsUser is None or len(targetPlatformsUser.targetPlatforms.targetPlatform) == 0:
        return None
    else:
        for item in targetPlatformsUser.targetPlatforms.targetPlatform:
            if (item.name == targetPlatformName):
                return item
    return None


def assign_target_platform_account(credAccount, targetPlatformName):
    myTargetPlatform = targetPlatform()
    myTargetPlatform.name = targetPlatformName
    credAccount.targetPlatform = myTargetPlatform
    return credAccount
