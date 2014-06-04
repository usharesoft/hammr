# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="UShareSoft"
import printer


def publish_vcd(pimage, builder):
        #doing field verification
        if not "orgName" in builder:
                printer.out("orgName in vcd builder not found", printer.ERROR)
                return
        if not "catalogName" in builder:
                printer.out("catalogName in vcd builder not found", printer.ERROR)
                return
        if not "imageName" in builder:
                printer.out("imageName in vcd builder not found", printer.ERROR)
                return
       
        pimage.credAccount.organizationName = builder["orgName"]
        pimage.credAccount.catalogId = builder["catalogName"]
        pimage.credAccount.displayName = builder["imageName"]
        return pimage

def publish_vcenter(pimage, builder):
        #doing field verification
        if not "datacenterName" in builder:
                printer.out("datacenterName in vcenter builder not found", printer.ERROR)
                return
        if not "cluster" in builder:
                printer.out("cluster in vcenter builder not found", printer.ERROR)
                return
        if not "datastore" in builder:
                printer.out("datastore in vcenter builder not found", printer.ERROR)
                return
        if not "imageName" in builder:
                printer.out("imageName in vcenter builder not found", printer.ERROR)
                return
       
        pimage.credAccount.clusterName = builder["cluster"]
        pimage.credAccount.datacenterName = builder["datacenterName"]
        pimage.credAccount.datastore = builder["datastore"]
        pimage.credAccount.displayName = builder["imageName"]
        return pimage
      
def publish_cloudstack(pimage, builder):
        #doing field verification
        if not "imageName" in builder:
                printer.out("imageName in cloudstack builder not found", printer.ERROR)
                return
        if not "zone" in builder:
                printer.out("zone in cloudstack builder not found", printer.ERROR)
                return
        if "publicImage" in builder:
                pimage.credAccount.publicImage = True if (builder["publicImage"]=="true") else False
        if "featured" in builder:
                pimage.credAccount.featuredEnabled = True if (builder["featured"]=="true") else False
        
        pimage.credAccount.displayName = builder["imageName"]
        pimage.credAccount.zoneName = builder["zone"]
        return pimage
    
    
def publish_cloudstack_qcow2(pimage, builder):
        return publish_cloudstack(pimage, builder)
    
def publish_cloudstack_vhd(pimage, builder):
        return publish_cloudstack(pimage, builder)
    
def publish_cloudstack_ova(pimage, builder):
        return publish_cloudstack(pimage, builder)    

def publish_susecloud(pimage, builder):
        #doing field verification
        if not "imageName" in builder:
                printer.out("imageName in susecloud builder not found", printer.ERROR)
                return
        if not "tenant" in builder:
                printer.out("tenant in susecloud builder not found", printer.ERROR)
                return
        if "description" in builder:
                pimage.credAccount.description = builder["description"]
        
        pimage.credAccount.displayName = builder["imageName"]
        pimage.credAccount.tenantName = builder["tenant"]
        if "publicImage" in builder:
                pimage.credAccount.publicImage = True if (builder["publicImage"]=="true") else False
        #if "paraVirtualMode" in builder:
        #        pimage.credAccount. = True if (builder["paraVirtualMode"]=="true") else False
        return pimage    
    
def publish_openstack(pimage, builder):
        #doing field verification
        if not "imageName" in builder:
                printer.out("imageName in openstack builder not found", printer.ERROR)
                return
        if not "tenant" in builder:
                printer.out("tenant in openstack builder not found", printer.ERROR)
                return
        if "description" in builder:
                pimage.credAccount.description = builder["description"]
        
        pimage.credAccount.displayName = builder["imageName"]
        pimage.credAccount.tenantName = builder["tenant"]
        if "publicImage" in builder:
                pimage.credAccount.publicImage = True if (builder["publicImage"]=="true") else False
        #if "paraVirtualMode" in builder:
        #        pimage.credAccount. = True if (builder["paraVirtualMode"]=="true") else False
        return pimage
    

def publish_ami(pimage, builder):
        #doing field verification
        if not "s3bucket" in builder:
                printer.out("s3bucket in AMI builder not found", printer.ERROR)
                return
        if not "region" in builder:
                printer.out("region in AMI builder not found", printer.ERROR)
                return
        
        pimage.credAccount.bucket = builder["s3bucket"]
        pimage.publishLocation = builder["region"]
        return pimage
    
    
def publish_azure(pimage, builder):
        #doing field verification
        if not "storageAccount" in builder:
                printer.out("region in Microsoft Azure not found", printer.ERROR)
                return
        
        pimage.credAccount.bucket = builder["storageAccount"]
        if "location" in builder:
                pimage.credAccount.zoneName = builder["location"]
                pimage.publishLocation = builder["location"]
                
        return pimage
    
def publish_flexiant(pimage, builder):
        #doing field verification
        if not "imageName" in builder:
                printer.out("imageName in flexiant builder not found", printer.ERROR)
                return
        if not "virtualDatacenter" in builder:
                printer.out("virtualDatacenter in flexiant builder not found", printer.ERROR)
                return
        if not "diskOffering" in builder:
                printer.out("diskOffering in flexiant builder not found", printer.ERROR)
                return
        
        pimage.credAccount.displayName = builder["imageName"]
        pimage.credAccount.datacenterName = builder["virtualDatacenter"]
        pimage.credAccount.category = builder["diskOffering"]
                
        return pimage
    
    
def publish_flexiant_kvm(pimage, builder):
        return publish_flexiant(pimage, builder)
    
def publish_flexiant_ova(pimage, builder):
        return publish_flexiant(pimage, builder)
    
def publish_flexiant_raw(pimage, builder):
        return publish_flexiant(pimage, builder)
    
    
def publish_abiquo(pimage, builder):
        #doing field verification
        if not "enterprise" in builder:
                printer.out("enterprise in abiquo builder not found", printer.ERROR)
                return
        if not "datacenter" in builder:
                printer.out("datacenter in abiquo builder not found", printer.ERROR)
                return
        if not "productName" in builder:
                printer.out("productName in abiquo builder not found", printer.ERROR)
                return
        if not "category" in builder:
                printer.out("category in abiquo builder not found", printer.ERROR)
                return
        if not "description" in builder:
                printer.out("description in abiquo builder not found", printer.ERROR)
                return
        
        pimage.credAccount.datacenterName = builder["datacenter"]
        pimage.credAccount.displayName = builder["productName"]        
        pimage.credAccount.category = builder["category"]        
        pimage.credAccount.organizationName = builder["enterprise"]
        pimage.credAccount.description = builder["description"]
                
        return pimage
    
def publish_nimbula(pimage, builder):
        #doing field verification
        if not "imageListName" in builder:
                printer.out("imageListName in nimbula builder not found", printer.ERROR)
                return
        if not "imageVersion" in builder:
                printer.out("imageVersion in nimbula builder not found", printer.ERROR)
                return
        if not "description" in builder:
                printer.out("description in nimbula builder not found", printer.ERROR)
                return        
        
        pimage.credAccount.imageVersion = builder["imageVersion"]
        pimage.credAccount.description = builder["description"]        
        pimage.credAccount.listName = builder["imageListName"]
                
        return pimage
    
def publish_nimbula_kvm(pimage, builder):
        return publish_nimbula(pimage, builder)
    
def publish_nimbula_esx(pimage, builder):
        return publish_nimbula(pimage, builder)
    
    
def publish_eucalyptus(pimage, builder):
        #doing field verification
        if not "imageName" in builder:
                printer.out("imageName in Eucalyptus builder not found", printer.ERROR)
                return
        if not "description" in builder:
                printer.out("description in Eucalyptus builder not found", printer.ERROR)
                return
        if not "bucket" in builder:
                printer.out("bucket in Eucalyptus builder not found", printer.ERROR)
                return
         
        pimage.credAccount.displayName = builder["imageName"]
        pimage.credAccount.bucket = builder["bucket"]
        pimage.credAccount.description = builder["description"]
        if "ramdisk" in builder and "kernelId" in builder:
                pimage.credAccount.ramdiskId = builder["ramdisk"]
                pimage.credAccount.kernelId = builder["kernelId"]
                        
        return pimage
    
def publish_eucalyptus_kvm(pimage, builder):
        return publish_eucalyptus(pimage, builder)
    
def publish_eucalyptus_xen(pimage, builder):
        return publish_eucalyptus(pimage, builder)
    
    
def publish_gce(pimage, builder):
        #doing field verification
        if not "computeZone" in builder:
                printer.out("computeZone in GCE builder not found", printer.ERROR)
                return
        if not "bucketLocation" in builder:
                printer.out("bucketLocation in GCE builder not found", printer.ERROR)
                return
        if not "bucket" in builder:
                printer.out("bucket in GCE builder not found", printer.ERROR)
                return
        if not "projectId" in builder:
                printer.out("projectId in GCE builder not found", printer.ERROR)
                return
        if not "storageClass" in builder:
                printer.out("storageClass in GCE builder not found", printer.ERROR)
                return
        if not "diskNamePrefix" in builder:
                printer.out("diskNamePrefix in AMI builder not found", printer.ERROR)
                return
            
        if "description" in builder:
                pimage.credAccount.description = builder["description"]
        
        pimage.credAccount.bucket = builder["bucket"]
        pimage.credAccount.tenantName = builder["projectId"]
        pimage.credAccount.category = builder["storageClass"]
        pimage.credAccount.displayName = builder["diskNamePrefix"]
        pimage.credAccount.zoneName = builder["computeZone"]
        pimage.publishLocation = builder["bucketLocation"]
        return pimage