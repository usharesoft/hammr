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

from texttable import Texttable
from ussclicore.utils import generics_utils

def scan_status(scan):
    if (scan.status.complete and not scan.status.error and not scan.status.cancelled):
        return "Done"
    elif(not scan.status.complete and not scan.status.error and not scan.status.cancelled):
        return str(scan.status.percentage)+"%"
    else:
        return "Error"

def scan_table(scanInstances, scan = None):
    table = Texttable(800)
    table.set_cols_dtype(["t","t","t","t"])
    table.header(["Id", "Name", "Status", "Distribution"])
    if scan:
        table.add_row([scan.dbId, "\t"+scan.name, scan_status(scan), "" ])
        return table
    for myScannedInstance in scanInstances:
        table.add_row([myScannedInstance.dbId, myScannedInstance.name, "", myScannedInstance.distribution.name + " "+ myScannedInstance.distribution.version + " " + myScannedInstance.distribution.arch])
        scans = generics_utils.order_list_object_by(myScannedInstance.scans.scan, "name")
        for lscan in scans:
            table.add_row([lscan.dbId, "\t"+lscan.name, scan_status(lscan), "" ])
    return table
