__author__ = 'Domenico Garlisi'

import sys
import time
import logging
from tempfile import NamedTemporaryFile
import shutil
import csv

sys.path.append('../../')

from controller.controller_utils import *
from controller.MeasurementManager import *
from controller.TestbedTopology import TestbedTopology
from traffic.traffic_module import *
from common.upihelper import unix_time_as_tuple, get_now_full_second
from upis.upi_rn import UPI_RN
from common.upihelper import Time
from helpers.application import ServerApplication, ClientApplication

"""
*************************************************************
WiSHFUL showcase 3 Experiment Controller
Load and Interference aware MAC adaptation
*************************************************************
"""



"""
We maintain a csv file (../../controller/testbed_nodes.csv) to store testbed nodes informations
Experiment controller write the nodes activity (e.g. traffic on/off)
WiSHFUL controller read node activity
"""
def register_traffic(station_index, value):
    filename = '../../controller/testbed_nodes.csv'
    tempfile = NamedTemporaryFile(delete=False)
    with open(filename, 'rb') as csvFile, tempfile:
        fieldnames = ['ip', 'hostname', 'role', 'traffic']
        reader = csv.DictReader(csvFile)
        writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
        writer.writeheader()
        row_number = 0
        for row in reader:
            if row_number == station_index:
                writer.writerow({'ip': row['ip'], 'hostname': row['hostname'], 'role': row['role'], 'traffic': value })
            else:
                writer.writerow({ 'ip': row['ip'], 'hostname': row['hostname'], 'role': row['role'], 'traffic': row['traffic'] })

            row_number += 1
    shutil.move(tempfile.name, filename)
    return


"""
Main control loop of global controller
"""
if __name__ == '__main__':

    """
    Init WiSHFUL framework
    """
    FORMAT = '> %(asctime)-15s %(message)s'    #FORMAT = "[%(asctime)-15s - %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    """
    *********************
    Wishful ShowCase 3
    Experiment Controller
    *********************
    We can use this in alternately of bash script or OML/OMF architecture
    """

    log.warning('*********** WISHFUL SC3 *************')
    log.warning('*********** starting Experiment Controller **********************')

    mytestbed = TestbedTopology("SC3",log)
    mytestbed.initializeTestbedTopology()       # discovery and allocate nodes
    mytestbed.initializeTestbedFunctions()      # set nodes rule: create network and association

    register_traffic(1, '0')
    register_traffic(2, '0')
    register_traffic(3, '0')

    """
    Managed traffic
    """
    log.warning('*********** START TRAFFIC **********************')

    serverApp0 = start_iperf_server_application(mytestbed.ap1, log, mytestbed)
    log.warn('IERF server started')

    clientApp0 = start_iperf_client_application(mytestbed.sta1, mytestbed.ap1, log, mytestbed)
    register_traffic(1, '1')
    log.warn('IERF client on STA1 started')
    time.sleep(40)

    clientApp1 = start_iperf_client_application(mytestbed.sta2, mytestbed.ap1, log, mytestbed)
    log.warn('IERF client on STA2 started')
    register_traffic(2, '1')
    time.sleep(40)

    clientApp2 = start_iperf_client_application(mytestbed.sta3, mytestbed.ap1, log, mytestbed)
    log.warn('IERF client on STA3 started')
    register_traffic(3, '1')

    while not ( clientApp0.isNewResult() and clientApp1.isNewResult() and clientApp2.isNewResult()):
        log.info('Waiting for app result')
        time.sleep(2)
    log.warn('------------------------------------------------------------')
    log.warn('Throughput result with ....:')
    #log.warn('\t AP : '+str(serverApp0.getResult()))
    log.warn('\tSTA1 -> AP : '+str(clientApp0.getResult()))
    log.warn('\tSTA2 -> AP : '+str(clientApp1.getResult()))
    log.warn('\tSTA3 -> AP : '+str(clientApp2.getResult()))
    log.warn('------------------------------------------------------------')

    register_traffic(1, '0')
    register_traffic(2, '0')
    register_traffic(3, '0')
