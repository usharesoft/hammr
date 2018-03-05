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

__author__="UShareSoft"

import os
import tempfile

VERSION="3.8.0.2"


TMP_WORKING_DIR=tempfile.gettempdir() + os.sep + "hammr-" + str(os.getpid())
HTTP_TIMEOUT=120

TEMPLATE_JSON_FILE_NAME="template.json"
TEMPLATE_JSON_NEW_FILE_NAME="template.json"
TEMPLATE_YAML_FILE_NAME="template.yml"
TEMPLATE_YAML_NEW_FILE_NAME="template.yml"

BUNDLE_JSON_FILE_NAME="bundle.json"
BUNDLE_JSON_NEW_FILE_NAME="bundle.json"
BUNDLE_YAML_FILE_NAME="bundle.yml"
BUNDLE_YAML_NEW_FILE_NAME="bundle.yml"

FOLDER_BUNDLES = "bundles";
FOLDER_CONFIGS = "config";
FOLDER_DEPLOYMENT_SCENARIO = "deploymentScenario";
FOLDER_LOGO = "logo";

URI_SCAN_BINARY="/resources/uforge-scan.bin"
SCAN_BINARY_NAME="uforge-scan.bin"

QUOTAS_SCAN="scan"
QUOTAS_TEMPLATE="appliance"
QUOTAS_GENERATION="generation"
QUOTAS_DISK_USAGE="diskusage"
