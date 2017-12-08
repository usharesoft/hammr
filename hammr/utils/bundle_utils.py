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

import os
import os.path
import ntpath
from ussclicore.utils import generics_utils, printer
from hammr.utils import constants
from uforge.objects.uforge import *

def check_bundle(bundle):
    if not "name" in bundle:
        printer.out("There is no attribute [name] for a [bundle]", printer.ERROR)
        return
    if not "version" in bundle:
        printer.out("no attribute [version] for [bundle]", printer.ERROR)
        return
    if not "files" in bundle:
        printer.out("no attribute [files] for [bundle]", printer.ERROR)
        return

    for file in bundle["files"]:
        bundle = check_files(bundle, file, 0)
        if bundle is None:
            return

    return bundle

def check_files(bundle, file, level):
    if not "name" in file:
        printer.out("There is no attribute [name] for a [file]", printer.ERROR)
        return
    if not "source" in file:
        printer.out("There is no attribute [source] for a [file]", printer.ERROR)
        return

    if level > 0 and "tag" in file and (file["tag"] == "ospkg" or file["tag"] == "bootscript"):
        printer.out("The file '" + file["name"] + ", with tag '" + file["tag"] + "' must be in the first level files section", printer.ERROR)
        return
    if ("bootOrder" in file or "bootType" in file) and (not "tag" in file or file["tag"] != "bootscript"):
        printer.out("There is the attribute [bootOrder] or [bootType] for file '" + file["name"] + "' but is not tagged as 'bootscript'", printer.ERROR)
        return
    if ("ownerGroup" in file or "rights" in file or "symlink" in file) and "tag" in file and file["tag"] != "softwarefile":
        printer.out("There is the attribute [ownerGroup], [rights] or [symlink] for file '" + file["name"] + "' but is not tagged as 'softwarefile'", printer.ERROR)
        return

    if "files" in file:
        if len(file["files"]) > 0:
            if "tag" in file and file["tag"] != "softwarefile":
                printer.out("The list of files is not empty for file '" + file["name"] + "' but is not tagged as 'softwarefile'", printer.ERROR)
                return
            elif not os.path.isdir(file["source"]):
                printer.out("The list of files is not empty for file '" + file["name"] + "' but [source] doesn't represent a folder", printer.ERROR)
                return

            for subFile in file["files"]:
                bundle = check_files(bundle, subFile, level + 1)

    return bundle

def recursivelyAppendToArchive(bundle, files, parentDir, checkList, archive_files):
    #must save the filepath before changing it after archive
    filePathBeforeTar = files["source"]
    if not "tag" in files or ("tag" in files and files["tag"] != "ospkg"):
        if files["source"] not in checkList:
            #add the source path to the check list
            checkList.append(files["source"])
            #if parentDir is a no empty path, add os.sep after. Else keep it as ""
            if parentDir:
                parentDir = parentDir + os.sep

            #add to list of file to tar
            file_tar_path=constants.FOLDER_BUNDLES + os.sep + generics_utils.remove_URI_forbidden_char(bundle["name"]) + os.sep + generics_utils.remove_URI_forbidden_char(bundle["version"]) + os.sep + parentDir + generics_utils.remove_URI_forbidden_char(ntpath.basename(files["source"]))
            archive_files.append([file_tar_path,files["source"]])
            #changing source path to archive related source path
            files["source"]=file_tar_path
        else:
            raise ValueError("Cannot have identical files in the bundles section: " + filePathBeforeTar)

    if "files" in files:
        for subFiles in files["files"]:
            checkList,archive_files = recursivelyAppendToArchive(bundle, subFiles, parentDir + ntpath.basename(files["source"]), checkList, archive_files)

    if (not "tag" in files or files["tag"] != "ospkg") and os.path.isdir(filePathBeforeTar):
        checkList,archive_files = processFilesFromFolder(bundle, files, filePathBeforeTar, parentDir + ntpath.basename(filePathBeforeTar), checkList, archive_files)

    return checkList, archive_files

def processFilesFromFolder(bundle, files, filePath, parentDir, checkList, archive_files):
    for subFiles in os.listdir(filePath):
        subFilesDict = dict({"name" : ntpath.basename(subFiles), "source" : filePath + os.sep + ntpath.basename(subFiles), "files" : []})
        #must save the filepath before changing it after archive
        subFilePathBeforeTar = subFilesDict["source"]
        if subFilesDict["source"] not in checkList:
            #add the source path to the check list
            checkList.append(subFilesDict["source"])
            #if parentDir is a no empty path, add os.sep after. Else keep it as ""
            if parentDir:
                parentDir = parentDir + os.sep

            #add to list of file to tar
            file_tar_path=constants.FOLDER_BUNDLES + os.sep + generics_utils.remove_URI_forbidden_char(bundle["name"]) + os.sep + generics_utils.remove_URI_forbidden_char(bundle["version"]) + os.sep + parentDir + generics_utils.remove_URI_forbidden_char(ntpath.basename(subFilesDict["source"]))
            archive_files.append([file_tar_path,subFilesDict["source"]])
            #changing source path to archive related source path and add it to files section of parent folder
            subFilesDict["source"] = file_tar_path
            files["files"].append(subFilesDict)

        if os.path.isdir(subFilePathBeforeTar):
            checkList,archive_files = processFilesFromFolder(bundle, subFilesDict, subFilePathBeforeTar, parentDir + ntpath.basename(subFilePathBeforeTar), checkList, archive_files)

    return checkList, archive_files