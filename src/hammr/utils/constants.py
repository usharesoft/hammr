# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="UShareSoft"

import os
import tempfile

VERSION="0.2.1"


TMP_WORKING_DIR=tempfile.gettempdir() + os.sep + "hammr-" + str(os.getpid())

TEMPLATE_JSON_FILE_NAME="template.json"
TEMPLATE_JSON_NEW_FILE_NAME="template.json"
FOLDER_BUNDLES = "bundles";
FOLDER_CONFIGS = "config";
FOLDER_DEPLOYMENT_SCENARIO = "deploymentScenario";
FOLDER_LOGO = "logo";

URI_SCAN_BINARY="/uforge-scan.bin"
SCAN_BINARY_NAME="uforge-scan.bin"

QUOTAS_SCAN="scan"
QUOTAS_TEMPLATE="appliance"
QUOTAS_GENERATION="generation"
QUOTAS_DISK_USAGE="diskusage"