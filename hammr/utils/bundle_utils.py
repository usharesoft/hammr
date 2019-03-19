# Copyright (c) 2007-2019 UShareSoft, All rights reserved
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

def recursively_append_to_archive(bundle, files, parent_dir, duplicate_check_list, archive_files):
    #must save the filepath before changing it after archive
    filePathBeforeTar = files["source"]

    if not "tag" in files or ("tag" in files and files["tag"] != "ospkg"):
        add_file_to_archive_and_update_file_source(bundle, files, parent_dir, duplicate_check_list, archive_files)

    if "files" in files:
        for subFiles in files["files"]:
            duplicate_check_list,archive_files = recursively_append_to_archive(
                bundle, subFiles, parent_dir + ntpath.basename(files["source"]), duplicate_check_list, archive_files)

    if (not "tag" in files or files["tag"] != "ospkg") and os.path.isdir(filePathBeforeTar):
        duplicate_check_list, archive_files = process_files_from_folder(
            bundle, files, filePathBeforeTar, parent_dir + ntpath.basename(filePathBeforeTar), duplicate_check_list, archive_files)

    return duplicate_check_list, archive_files

def process_files_from_folder(bundle, files, filePath, parentDir, duplicate_check_list, archive_files):
    for subFiles in os.listdir(filePath):
        subFilesDict = dict({"name" : ntpath.basename(subFiles), "source" : filePath + os.sep + ntpath.basename(subFiles), "files" : []})
        #must save the filepath before changing it after archive
        subFilePathBeforeTar = subFilesDict["source"]

        if add_file_to_archive_and_update_file_source(
                bundle, subFilesDict, parentDir, duplicate_check_list, archive_files, False):
            files["files"].append(subFilesDict)

        if os.path.isdir(subFilePathBeforeTar):
            duplicate_check_list,archive_files = process_files_from_folder(
                bundle, subFilesDict, subFilePathBeforeTar, parentDir + ntpath.basename(subFilePathBeforeTar),
                duplicate_check_list, archive_files)

    return duplicate_check_list, archive_files

def add_file_to_archive_and_update_file_source(bundle, file, parent_dir, duplicate_check_list,  archive_files, fail_on_duplicates=True):
    file_tar_path = build_file_tar_path(bundle, file, parent_dir)
    if file_tar_path not in duplicate_check_list:
        duplicate_check_list.append(file_tar_path)
        archive_files.append([file_tar_path, file["source"]])
        # changing source path to archive related source path
        file["source"] = file_tar_path
        return True
    elif fail_on_duplicates:
        raise ValueError(
            "Cannot have identical files in the bundles section: " + file_tar_path + " from " + file["source"])
    return False

def build_file_tar_path(bundle, file, parent_dir):
    # if parentDir is a no empty path or already ending with os.sep, add os.sep at the end
    if parent_dir and not parent_dir.endswith(os.sep):
        parent_dir = parent_dir + os.sep
    return constants.FOLDER_BUNDLES + os.sep + generics_utils.remove_URI_forbidden_char(bundle["name"]) \
                  + os.sep + generics_utils.remove_URI_forbidden_char(bundle["version"]) \
                  + os.sep + parent_dir \
                  + generics_utils.remove_URI_forbidden_char(ntpath.basename(file["name"]))
