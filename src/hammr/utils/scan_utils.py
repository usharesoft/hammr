__author__ = "UShareSoft"

from texttable import Texttable
import generics_utils

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
        scans = generics_utils.oder_list_object_by(myScannedInstance.get_scans().get_scan(), "name")
        for lscan in scans:
            table.add_row([lscan.dbId, "\t"+lscan.name, scan_status(lscan), "" ])
    return table
