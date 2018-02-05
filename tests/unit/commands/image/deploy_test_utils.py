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
from hammr.commands.deploy.deploy import OpStatus
from uforge.application import Api

from hammr.commands.image.image import Image
from hammr.utils import constants


def prepare_image():
    i = Image()
    i.api = Api("url", username="username", password="password", headers=None,
                disable_ssl_certificate_validation=False, timeout=constants.HTTP_TIMEOUT)
    i.login = "login"
    i.password = "password"
    return i

def str_list_to_opStatus_list(strStatusList):
    res = []
    for strStatus in strStatusList:
        opStatus = OpStatus()
        opStatus.message = strStatus
        res.append(opStatus)
    return res

def prepare_mock_deploy(deployment, pimages, source, statusList, mock_get_deployment, mock_get, mock_api_deploy,
                        mock_get_deploy_status, mock_api_pimg_getall):
    mock_api_deploy.return_value = deployment
    mock_get_deployment.return_value = deployment
    mock_get.return_value = source
    mock_api_pimg_getall.return_value = pimages
    mock_get_deploy_status.side_effect = str_list_to_opStatus_list(statusList)
