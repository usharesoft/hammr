# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import ntpath

from uforge.objects.xsd0 import *
import printer

__author__="UShareSoft"

def openstack(myCredAccount, account):
        #doing field verification
        if not "username" in account:
                printer.out("username in openstack account not found", printer.ERROR)
                return
        if not "password" in account:
                printer.out("catalogName in openstack account not found", printer.ERROR)
                return
        if not "endpoint" in account:
                printer.out("endpoint for openstack account not found", printer.ERROR)
                return
        if not "keystoneEndpoint" in account:
                printer.out("keystoneEndpoint for openstack account not found", printer.ERROR)
                return
        if not "name" in account:
                printer.out("name for openstack account not found", printer.ERROR)
                return
        
        myCredAccount.type_ = "openstack"
        myCredAccount.login = account["username"]
        myCredAccount.password = account["password"]
        myCredAccount.serverUrl = account["endpoint"]
        myCredAccount.keystoneUrl = account["keystoneEndpoint"]
        myCredAccount.name = account["name"]
        return myCredAccount
    
def susecloud(myCredAccount, account):
        #doing field verification
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
        
        myCredAccount.type_ = "susecloud"
        myCredAccount.login = account["username"]
        myCredAccount.password = account["password"]
        myCredAccount.serverUrl = account["endpoint"]
        myCredAccount.keystoneUrl = account["keystoneEndpoint"]
        myCredAccount.name = account["name"]
        return myCredAccount
    
    
def cloudstack_qcow2(myCredAccount, account):
        return cloudstack(myCredAccount, account)
    
def cloudstack_vhd(myCredAccount, account):
        return cloudstack(myCredAccount, account)
    
def cloudstack_ova(myCredAccount, account):
        return cloudstack(myCredAccount, account)    

def cloudstack(myCredAccount, account):
        #doing field verification
        if not "publicKey" in account:
                printer.out("publicKey in cloudstack account not found", printer.ERROR)
                return
        if not "secretKey" in account:
                printer.out("secretKey in cloudstack account not found", printer.ERROR)
                return
        if not "endpoint" in account:
                printer.out("endpoint for cloudstack account not found", printer.ERROR)
                return
        if not "name" in account:
                printer.out("name for cloudstack account not found", printer.ERROR)
                return
        
        myCredAccount.type_ = "cloudcom"
        myCredAccount.publicAPIKey = account["publicKey"]
        myCredAccount.secretAPIKey = account["secretKey"]
        myCredAccount.serverUrl = account["endpoint"]
        myCredAccount.name = account["name"]
        return myCredAccount
    
    
def ami(myCredAccount, account):
        #doing field verification
        if not "x509Cert" in account:
                printer.out("x509Cert in ami account not found", printer.ERROR)
                return
        if not "x509PrivateKey" in account:
                printer.out("x509PrivateKey in ami account not found", printer.ERROR)
                return
        if not "accessKey" in account:
                printer.out("accessKey in ami account not found", printer.ERROR)
                return
        if not "secretAccessKey" in account:
                printer.out("secretAccessKey in ami account not found", printer.ERROR)
                return
        if not "accountNumber" in account:
                printer.out("accountNumber for ami account not found", printer.ERROR)
                return
        if not "name" in account:
                printer.out("name for ami account not found", printer.ERROR)
                return
        
        myCredAccount.type_ = "aws"
        myCredAccount.accountNumber = account["accountNumber"]
        myCredAccount.secretAccessKeyID = account["secretAccessKey"]
        myCredAccount.accessKeyID = account["accessKey"]
        myCredAccount.name = account["name"]
        
        myCertificates = certificates()
        myCredAccount.certificates = myCertificates
        
        try:
                myCertificate = certificate()
                with open (account["x509Cert"], "r") as myfile:
                        myCertificate.certStr=myfile.read()
                myCertificate.type_ = "x509"        
                myCertificate.name = ntpath.basename(account["x509Cert"])
                myCertificates.add_certificate(myCertificate)
                myCertificate = certificate()
                with open (account["x509PrivateKey"], "r") as myfile:
                        myCertificate.certStr=myfile.read()
                myCertificate.type_ = "ec2PrivateKey"        
                myCertificate.name = ntpath.basename(account["x509PrivateKey"])
                myCertificates.add_certificate(myCertificate)        
        
            
                if "keyPairPrivateKey" in account:
                        myCertificate = certificate()
                        with open (account["keyPairPrivateKey"], "r") as myfile:
                                myCertificate.certStr=myfile.read()
                        myCertificate.type_ = "ec2KeyPairPrivateKey"        
                        myCertificate.name = ntpath.basename(account["keyPairPrivateKey"])
                        myCertificates.add_certificate(myCertificate)
                        
                        myCredAccount.keyPairName = os.path.splitext(myCertificate.name)[0]
                
        except IOError as e:
                printer.out("File error: "+str(e), printer.ERROR)
                return
        
        return myCredAccount
    
def azure(myCredAccount, account):
        #doing field verification
        if not "rsaPrivateKey" in account:
                printer.out("rsaPrivateKey in azure account not found", printer.ERROR)
                return
        if not "certKey" in account:
                printer.out("certKey in azure account not found", printer.ERROR)
                return
        if not "subscriptionId" in account:
                printer.out("subscriptionId for azure account not found", printer.ERROR)
                return
        if not "name" in account:
                printer.out("name for azure account not found", printer.ERROR)
                return
        
        myCredAccount.type_ = "azure"
        myCredAccount.accountNumber = account["subscriptionId"]
        myCredAccount.name = account["name"]
        
        myCertificates = certificates()
        myCredAccount.certificates = myCertificates
        
        try:
                myCertificate = certificate()
                with open (account["rsaPrivateKey"], "r") as myfile:
                        myCertificate.certStr=myfile.read()
                myCertificate.type_ = "azureRSAKey"        
                myCertificate.name = ntpath.basename(account["rsaPrivateKey"])
                myCertificates.add_certificate(myCertificate)
                myCertificate = certificate()
                with open (account["certKey"], "r") as myfile:
                        myCertificate.certStr=myfile.read()
                myCertificate.type_ = "azureCertKey"        
                myCertificate.name = ntpath.basename(account["certKey"])
                myCertificates.add_certificate(myCertificate)        
        
                
        except IOError as e:
                printer.out("File error: "+str(e), printer.ERROR)
                return
        
        return myCredAccount
    
    
    
def eucalyptus_kvm(myCredAccount, account):
        return eucalyptus(myCredAccount, account)
    
def eucalyptus_xen(myCredAccount, account):
        return eucalyptus(myCredAccount, account)
    
def eucalyptus(myCredAccount, account):
        #doing field verification
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
        
        myCredAccount.type_ = "ews"        
        myCredAccount.accountNumber = account["accountNumber"]
        myCredAccount.name = account["name"]
        myCredAccount.hostname = account["endpoint"]
        myCredAccount.secretAccessKeyID = account["secretKey"]
        myCredAccount.accessKeyID = account["queryId"]
        
        myCertificates = certificates()
        myCredAccount.certificates = myCertificates
        
        try:
                myCertificate = certificate()
                with open (account["x509Cert"], "r") as myfile:
                        myCertificate.certStr=myfile.read()
                myCertificate.type_ = "x509"        
                myCertificate.name = ntpath.basename(account["x509Cert"])
                myCertificates.add_certificate(myCertificate)
                myCertificate = certificate()
                with open (account["x509PrivateKey"], "r") as myfile:
                        myCertificate.certStr=myfile.read()
                myCertificate.type_ = "ec2PrivateKey"        
                myCertificate.name = ntpath.basename(account["x509PrivateKey"])
                myCertificates.add_certificate(myCertificate)
                myCertificate = certificate()
                with open (account["cloudCert"], "r") as myfile:
                        myCertificate.certStr=myfile.read()
                myCertificate.type_ = "eucCert"        
                myCertificate.name = ntpath.basename(account["cloudCert"])
                myCertificates.add_certificate(myCertificate)
        
                
        except IOError as e:
                printer.out("File error: "+str(e), printer.ERROR)
                return
        
        return myCredAccount
    
def abiquo(myCredAccount, account):
        #doing field verification
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
        
        myCredAccount.type_ = "abiquo"
        myCredAccount.login = account["username"]
        myCredAccount.password = account["password"]
        myCredAccount.hostname = account["hostname"]
        myCredAccount.name = account["name"]
        return myCredAccount
    
    
def nimbula(myCredAccount, account):
        #doing field verification
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
        
        myCredAccount.type_ = "nimbula"
        myCredAccount.login = account["username"]
        myCredAccount.password = account["password"]
        myCredAccount.serverUrl = account["endpoint"]
        myCredAccount.name = account["name"]
        return myCredAccount
    
def flexiant(myCredAccount, account):
        #doing field verification
        if not "password" in account:
                printer.out("password in flexiant account not found", printer.ERROR)
                return
        if not "username" in account:
                printer.out("username in flexiant account not found", printer.ERROR)
                return
        if not "wsdlURL" in account:
                printer.out("wsdlURL for flexiant account not found", printer.ERROR)
                return
        if not "name" in account:
                printer.out("name for flexiant account not found", printer.ERROR)
                return
        
        myCredAccount.type_ = "flexiant"
        myCredAccount.login = account["username"]
        myCredAccount.password = account["password"]
        
        try:
                myCredAccount.userUUID = (myCredAccount.login).split('/')[1]
        except:
                printer.out(account["username"]+ " is not a valid Flexiant username", printer.ERROR)
                return 
        
        myCredAccount.wsdlLocation = account["wsdlURL"]
        myCredAccount.name = account["name"]
        return myCredAccount
    
def flexiant_kvm(myCredAccount, account):
        return flexiant(myCredAccount, account)
    
def flexiant_ova(myCredAccount, account):
        return flexiant(myCredAccount, account)
    
def flexiant_raw(myCredAccount, account):
        return flexiant(myCredAccount, account)
    
def vcd(myCredAccount, account):
        #doing field verification
        if not "hostname" in account:
                printer.out("hostname in vcd account not found", printer.ERROR)
                return
        if not "username" in account:
                printer.out("username in vcd account not found", printer.ERROR)
                return    
        if not "password" in account:
                printer.out("password in vcd account not found", printer.ERROR)
                return
        if not "name" in account:
                printer.out("name in vcd account not found", printer.ERROR)
                return
            
        if "proxyHostname" in account:
                myCredAccount.proxyHost = account["proxyHostname"]
        if "proxyPort" in account:
                myCredAccount.proxyPort = account["proxyPort"]
        if "port" in account:
            port = int(account["port"])
        else:
            port=443
        
        myCredAccount.type_ = "vclouddirector"
        myCredAccount.name = account["name"]
        myCredAccount.login = account["username"]
        myCredAccount.password = account["password"]
        myCredAccount.hostname = account["hostname"]
        myCredAccount.port = port
        
        return myCredAccount
    
def vcenter(myCredAccount, account):
        #doing field verification
        if not "hostname" in account:
                printer.out("hostname in vcenter account not found", printer.ERROR)
                return
        if not "username" in account:
                printer.out("username in vcenter account not found", printer.ERROR)
                return    
        if not "password" in account:
                printer.out("password in vcenter account not found", printer.ERROR)
                return
        if not "name" in account:
                printer.out("name in vcenter account not found", printer.ERROR)
                return
            
        if "proxyHostname" in account:
                myCredAccount.proxyHost = account["proxyHostname"]
        if "proxyPort" in account:
                myCredAccount.proxyPort = account["proxyPort"]
        if "port" in account:
                port = int(account["port"])
        else:
                port=443
        
        myCredAccount.type_ = "vsphere"
        myCredAccount.name = account["name"]
        myCredAccount.login = account["username"]
        myCredAccount.password = account["password"]
        myCredAccount.hostname = account["hostname"]
        myCredAccount.port = port
        return myCredAccount
    
def gce(myCredAccount, account):
        #doing field verification
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
                with open (account["cert"], "r") as myfile:
                        myCertificate.certStr=myfile.read()
                myCertificate.type_ = "googleCertificate"
                myCertificate.name = ntpath.basename(account["cert"])
                myCertificates.add_certificate(myCertificate)
                
        except IOError as e:
                printer.out("File error: "+str(e), printer.ERROR)
                return
        
        return myCredAccount