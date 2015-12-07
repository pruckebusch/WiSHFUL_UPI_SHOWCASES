#!/usr/bin/python
import sys

__author__ = 'A. Zubow, S. Zehl'

import time
from common.constants import RPC_PORT
from common.upihelper import unix_time_as_tuple, get_now_full_second
from upis.upi_g import UPI_G
from master.master import GlobalManager, Node
from upis.upi_rn import UPI_RN
import logging
from datetime import datetime, date, timedelta
from functools import partial
import numpy
from helpers.mac_layer import HybridTDMACSMAMac, AccessPolicy
from helpers.helper import NetworkHelper, NetworkFunctionHelper
from helpers.helper import RadioHelper
from helpers.application import ServerApplication, ClientApplication
import signal
from common.upihelper import Time
import pickle

"""
EU project WISHFUL

Wishful controller used for showcase 1 - "Efficient Airtime Management in Enterprise IEEE 802.11"

The scenario consists of two APs and single STA with the radio interfaces imitating two STAs.

        AP1-^ ------- ^-STA-^ ------- ^-AP2

The solution uses global control and consists of three steps:
(1) Detection of a hidden-node scenario: the two APs are outside of their carrier sensing range and the STA is in
communication range of the two APs -> UPI_G::execNetworkFunction()
(2) Measuring the DL TCP/IP performance of the baseline, i.e. standard 802.11 MAC protocol
(3) Setting up the hybrid TDMA/CSMA MAC protocol and assigning different time slots to both radio links, i.e. AP1-STA1
and AP2-STA2 and again measuring the performance.
"""


"""
Helper functions tests for each pair of nodes whether there are in carrier sensing range or not.
:return a matrix
"""
def test_is_incsrange_global(networkFuncHelper, wirelessNodes, wifi_intf, rfCh):
    log.info('test_is_incsrange_global')

    CSmat = numpy.zeros((len(wirelessNodes), len(wirelessNodes)))
    try:
        # UPI_G call
        isInCss = networkFuncHelper.getNodesInCarrierSensingRange(wirelessNodes, wifi_intf, rfCh)

        for i in range(0, len(isInCss)):
            isInCs = isInCss[i]

            if isInCs[2]:
                log.info('Nodes %s and %s are IN carrier sensing range.' % (str(isInCs[0]), str(isInCs[1])))
            else:
                log.info('Nodes %s and %s are OUTSIDE carrier sensing range.' % (str(isInCs[0]), str(isInCs[1])))

            rowIdx = wirelessNodes.index(isInCs[0])
            colIdx = wirelessNodes.index(isInCs[1])

            CSmat[rowIdx, colIdx] = 1 if isInCs[2] else 0
            # symmetrical
            CSmat[colIdx, rowIdx] = CSmat[rowIdx, colIdx]
    except Exception as e:
        log.fatal("An error occurred : %s" % e)

    return CSmat

"""
Helper functions tests for each pair of nodes whether there are in communication range or not.
:return a matrix
"""
def test_is_incommrange_global(networkFuncHelper, wirelessNodes, wifi_intf, rfCh):
    log.info('test_is_incommrange_global')

    CRmat = numpy.zeros((len(wirelessNodes), len(wirelessNodes)))
    try:
        isInComms = networkFuncHelper.getNodesInCommunicationRange(wirelessNodes, wifi_intf, rfCh)

        for i in range(0, len(isInComms)):
            isInComm = isInComms[i]
            if isInComm[2]:
                log.info('Nodes %s and %s are IN communication range.' % (str(isInComm[0]), str(isInComm[1])))
            else:
                log.info('Nodes %s and %s are OUTSIDE communication range.' % (str(isInComm[0]), str(isInComm[1])))

            rowIdx = wirelessNodes.index(isInComm[0])
            colIdx = wirelessNodes.index(isInComm[1])

            CRmat[rowIdx, colIdx] = 1 if isInComm[2] else 0
            # symmetrical
            CRmat[colIdx, rowIdx] = CRmat[rowIdx, colIdx]
    except Exception as e:
        log.fatal("An error occurred : %s" % e)

    return CRmat

"""
Main control loop of global controller for showcase 1.
"""
if __name__ == '__main__':

    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT)
    log = logging.getLogger()
    log.setLevel(logging.WARN)
    log.info('Master controller started')

    # name of the experiment group; only nodes of this group can be controlled
    exp_group_name = "MyWishFulTest"

    log.debug('SC1 global controller started for group %s', exp_group_name)

    # get reference to global UPI
    global_mgr = GlobalManager(exp_group_name)

    netHelper = NetworkHelper(global_mgr)
    radioHelper = RadioHelper(global_mgr)
    networkFuncHelper = NetworkFunctionHelper(global_mgr)

    # nodes under control
    nodes = []
    node0 = Node("192.168.103.125")  # nuc2
    node1 = Node("192.168.103.134")  # nuc3
    laptop = Node("192.168.103.232")  # experiment laptop

    nodes.append(node0)
    nodes.append(node1)
    nodes.append(laptop)

    # node discovery: wait until all specified nodes are available
    discovered_nodes = global_mgr.waitForNodes(nodes)

    expectedNodeIps = [node.getIpAddress() for node in discovered_nodes]
    log.info('Expected Wishful nodes: %s' % str(expectedNodeIps))
    nodeRpcIds = [str(node._rpcId) for node in discovered_nodes]
    log.info('Discovered Wishful nodes: %s' % str(nodeRpcIds))

    # node0 and node1 are the APs
    APNodes = [node0, node1]
    
    # the laptop is our client station
    STANodes = [laptop]

    # start thread for callback, have to be done after some peers are available
    global_mgr.startResultCollector()

    # 802.11 configuration, i.e. radio channel and name of the WiFi interface
    rfCh = 36
    wifi_iface = 'mon2'

    log.warn('************************************************************')
    log.warn('WISHFUL Showcase (1)')
    log.warn('************************************************************')

    BO_DURATION = 5
    MAX_TRIES = 1
    # try at most three times to find a hidden node scenario
    for rr in range(MAX_TRIES):
        log.warn("-> Running: Carrier Sensing Range Test")
        CSmat = test_is_incsrange_global(networkFuncHelper, APNodes, wifi_iface, rfCh)

        # do the checks
        ap1Idx = APNodes.index(APNodes[0])
        ap2Idx = APNodes.index(APNodes[1])
        log.info('APs must be outside CS range ...')
        if CSmat[ap1Idx, ap2Idx] == 1:
            log.info('FAILED ... backoff for %d sec.' % BO_DURATION)
            time.sleep(BO_DURATION)
            continue

        log.warn('CS Test Passed (CS matrix):')
        log.warn(CSmat)

        time.sleep(1)

        log.warn("-> Running: Communication Range Test")
        CRmat = test_is_incommrange_global(networkFuncHelper, nodes, wifi_iface, rfCh)
        log.warn('CR Test Passed (CR matrix):')
        log.warn(CRmat)

        log.info('STA must be inside communication range of both APs ...')
        staIdx = nodes.index(STANodes[0])
        if CRmat[ap1Idx, staIdx] == 0 or CRmat[ap2Idx, staIdx] == 0:
            log.info('FAILED ... backoff for %d sec.' % BO_DURATION)
            time.sleep(BO_DURATION)
            continue

        log.info('OK.')
        break

    if rr == MAX_TRIES:
        log.warning("No hidden node configuration found")
        global_mgr.stop()
    log.warn('! Hidden node configuration found !')

    time.sleep(2)
        
    log.info('(Re)connect to both AP Nodes')
    
    UPIfunc = UPI_RN.setParameterLowerLayer
    # remote function args
    UPIargs = {'cmd' : UPI_RN.IEEE80211_CONNECT_TO_AP, 'iface' : 'wifi2', 'ssid' : 'effman-nuc2'}

    rvalue = global_mgr.runAt(STANodes, UPIfunc, UPIargs, None)

    UPIfunc = UPI_RN.setParameterLowerLayer
    # remote function args
    UPIargs = {'cmd' : UPI_RN.IEEE80211_CONNECT_TO_AP, 'iface' : 'wifi3', 'ssid' : 'effman-nuc3'}

    rvalue = global_mgr.runAt(STANodes, UPIfunc, UPIargs, None)
    
    log.warn("-> Running: Iperf Throughput Test")
    time.sleep(5)

    log.info('Installing iperf applications in notebook')
    serverApp0 = ServerApplication()
    serverApp0.setStartTime(Time.Now() + Time.Seconds(2))
    serverApp0.setBind("192.168.2.202")
    serverApp0.setProtocol("TCP")
    netHelper.installApplication(laptop, serverApp0)
    
    serverApp1 = ServerApplication()
    serverApp1.setStartTime(Time.Now() + Time.Seconds(2))
    serverApp1.setBind("192.168.3.203")
    serverApp1.setProtocol("TCP")
    netHelper.installApplication(laptop, serverApp1)
    
    # node0
    clientApp0 = ClientApplication()
    clientApp0.setStartTime(Time.Now() + Time.Seconds(5))
    clientApp0.setDestination("192.168.2.202")
    clientApp0.setProtocol("TCP")
    netHelper.installApplication(node0, clientApp0)
    
    # node1
    clientApp1 = ClientApplication()
    clientApp1.setStartTime(Time.Now() + Time.Seconds(5))
    clientApp1.setDestination("192.168.3.203")
    clientApp1.setProtocol("TCP")
    netHelper.installApplication(node1, clientApp1)
    
    while not (clientApp0.isNewResult() and clientApp1.isNewResult() and serverApp0.isNewResult() and serverApp1.isNewResult()):
        log.info('Waiting for app result')
        time.sleep(2)
    log.warn('------------------------------------------------------------')
    log.warn('Throughput result with standard CSMA/CA:')
    log.warn('\tAP0 -> STA : '+str(clientApp0.getResult()))
    log.warn('\tAP1 -> STA : '+str(clientApp1.getResult()))
    log.warn('------------------------------------------------------------')

    log.warn('Starting Hybrid MAC Configuration')
        
    log.info('Get HW address of both interfaces of STA')
    # get my MAC HW address
    hwAddr0 = radioHelper.getHwAddrRemote(laptop, 'wifi2')
    hwAddr1 = radioHelper.getHwAddrRemote(laptop, 'wifi3')

    # hybrid MAC parameter
    total_slots = 10
    slot_duration = 20000
    iface = 'wifi0'

    log.warn("-> Running: Hybrid MAC Processor Installation")
    log.info('Hybrid TDMA/CSMA MAC conf: #slots=%d, slot_dur=%d ms' % (total_slots, (slot_duration/1e3)))

    # install hybrid MAC on each wireless node
    macs = []
    for ni in range(len(nodes)-1):
        log.info('Installing hybrid MAC on ... %s' % str(nodes[ni].getIpAddress()))

        # create new MAC for each node
        mac = HybridTDMACSMAMac(no_slots_in_superframe=total_slots, slot_duration_ns=slot_duration)
        macs.append(mac)

        if ni==0:
            # node0: guards=0,5,6,7,8,9, BE=1,2,3,4
            be_slots = [1,2,3,4]
            dstHWAddr = hwAddr0
        else:
            # node1: guards=0,1,2,3,4,5, BE=6,7,8,9
            be_slots = [6,7,8,9]
            dstHWAddr = hwAddr1
    
        # assign access policies to each slot in superframe
        for slot_nr in range(total_slots):
            if slot_nr in be_slots:
                acBE = AccessPolicy()
                acBE.addDestMacAndTosValues(dstHWAddr, 0)
                mac.addAccessPolicy(slot_nr, acBE)
            else:
                acGuard = AccessPolicy()
                acGuard.disableAll() # guard slot
                mac.addAccessPolicy(slot_nr, acGuard)
    
        if radioHelper.installMacProcessor(nodes[ni], iface, mac):
            log.info('Hybrid MAC installed on %s ... OK' % str(nodes[ni].getIpAddress()))
            log.info('%s' % mac.printConfiguration())
        else:
            log.error('Unable to instantiate hybrid MAC on %s' % str(nodes[ni].getIpAddress()))
            log.error('Aborting ...')
            sys.exit(0)
    
    time.sleep(5)
    log.warn("-> Running: Iperf Throughput Test")

    log.info('Installing applications in notebook')
    serverApp0 = ServerApplication()
    serverApp0.setStartTime(Time.Now() + Time.Seconds(2))
    serverApp0.setBind("192.168.2.202")
    serverApp0.setProtocol("TCP")
    netHelper.installApplication(laptop, serverApp0)
    
    serverApp1 = ServerApplication()
    serverApp1.setStartTime(Time.Now() + Time.Seconds(2))
    serverApp1.setBind("192.168.3.203")
    serverApp1.setProtocol("TCP")
    netHelper.installApplication(laptop, serverApp1)
    
    time.sleep(10)
    
    # node0
    clientApp0 = ClientApplication()
    clientApp0.setStartTime(Time.Now() + Time.Seconds(4))
    clientApp0.setDestination("192.168.2.202")
    clientApp0.setProtocol("TCP")
    netHelper.installApplication(node0, clientApp0)
    
    # node1
    clientApp1 = ClientApplication()
    clientApp1.setStartTime(Time.Now() + Time.Seconds(4))
    clientApp1.setDestination("192.168.3.203")
    clientApp1.setProtocol("TCP")
    netHelper.installApplication(node1, clientApp1)
    
    while not (clientApp0.isNewResult() and clientApp1.isNewResult() and serverApp0.isNewResult() and serverApp1.isNewResult()):
        log.info('Waiting for app result')
        time.sleep(2)
    
    log.warn('------------------------------------------------------------')
    log.warn('Throughput result with Hybrid MAC: ')
    log.warn('\tAP0 -> STA : '+str(clientApp0.getResult()))
    log.warn('\tAP1 -> STA : '+str(clientApp1.getResult()))

    log.warn('------------------------------------------------------------')

    # uninstall hybrid MAC
    for ni in range(len(nodes)-1):
        if not radioHelper.uninstallMacProcessor(nodes[ni], iface, macs[ni]):
            log.error('Failed to uninstall MAC processor ...')

    global_mgr.stop()
    log.warning("... done")
