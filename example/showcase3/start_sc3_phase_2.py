__author__ = 'Domenico Garlisi'

import sys
import time
import logging
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
WiSHFUL showcase 3 implementation
Load and Interference aware MAC adaptation
*************************************************************
"""

def run_local_controller(mytestbed, disable=0):

    """
    Custom function used to implement local WiSHFUL controller
    """
    def customLocalCtrlFunction(myargs):

        import time
        import logging

        # references to Wishful framework
        global upiRNImpl # interface to UPI_R/N implementation
        global upiHCImpl # interface used for communication with global controller and control runtime

        log = logging.getLogger()
        log.warning('*********** WISHFUL SC3 *************')
        log.warning('*********** starting local WiSHFUL controller **********************')
        last_freezing_number = 0


        b = 0.1
        a = 0.1
        last_count_freezing = 0
        CWMIN = 31 #15
        CWMAX = 1023
        T = 0.5 #0.1
        ipt = 0
        cw_f = CWMIN
        cycle_update = 0

        while not upiHCImpl.stopIsSet():

            UPIargs = {'iface' : 'wlan0' }
            ip_address = upiRNImpl.getIfaceIpAddr(UPIargs)
            cycle_update += 1

            #get freezing number
            #UPIfunc = UPI_RN.getMonitor
            UPIargs = {'KEY' : (UPI_RN.NUM_FREEZING_COUNT, 'wlan0' )}
            current_freezing_number = upiRNImpl.getMonitor(UPIargs)
            count_freezing = current_freezing_number[0]

            #Find/Compute CW good
            delta_freezing = count_freezing - last_count_freezing
            if delta_freezing < 0 :
                delta_freezing = 65535 - last_count_freezing + count_freezing
            last_count_freezing = count_freezing

            ipt = ipt + a * (delta_freezing - ipt)
            # #targetcw = -0.0131 * ipt ** 2 + 3.2180 * ipt + 13.9265;  # determine the target CW for this IPT
            targetcw = -1.3539 * ipt ** 2 + 7.6655 * ipt + 15.4545;  # determine the target CW for this IPT ver 25-11-2015 on TTILAB with 2,4,6 nodes samples.
            # calculate new smoothed CW
            cw_f = cw_f + b * (targetcw - cw_f);
            cw = round(cw_f);
            cw = int(cw)
            cw = max(cw,CWMIN);
            cw = min(cw,CWMAX);
            #cw = 50

            #update CW value
            UPIargs = {'KEY' : (UPI_RN.CSMA_CW, UPI_RN.CSMA_CW_MIN, UPI_RN.CSMA_CW_MAX, 'wlan0' ), 'VALUE' : [cw, cw, cw ]}
            upiRNImpl.setParameterLowerLayer(UPIargs)

            if not(cycle_update % 10):
                #communicate with global controller by passing control message
                upiHCImpl.transmitCtrlMsgUpstream( { "FREEZING_NUMBER" : [current_freezing_number], "IP_ADDRESS" : (ip_address) } )
                log.info('current freezing number : %d' % (last_count_freezing))

            #wait next update time
            time.sleep(T)

        return 'Local WiSHFUL Controller END'

    """
    Custom callback function used to receive result values from scheduled calls, i.e. if you schedule the execution of a
    particular UPI_R/N function in the future this callback allows you to be informed about any function return values.
    """
    numCBs = {}
    numCBs['res'] = 0
    # use in while to lern if the local logic stopped e.g.
    # while numCBs['res'] < 2:

    def resultCollector(json_message, funcId):
        log.info('json: %s' % json_message)
        time_val = json_message['time']
        peer_node = json_message['peer']
        messagedata = json_message['msg']
        log.info('Callback %d: Local controller receives data msg at %s from %s : %s' % (funcId, str(time_val), peer_node, messagedata))
        numCBs['res'] = numCBs['res'] + 1

    """
    Custom callback function used to receive control feedback results from local controllers.
    """
    def ctrlMsgCollector(json_message):
        time_val = json_message['time']
        peer_node = json_message['peer']
        msg_data = json_message['msg']
        remote_wlan_ipAddress = msg_data['IP_ADDRESS']
        measurement_types = 'FREEZING_NUMBER'
        measurement = msg_data['FREEZING_NUMBER']
        log.info('Global controller receives ctrl msg at %s from %s : %s' % (str(time_val), peer_node, str(msg_data) ))

        # add measurement on nodes element
        for node in mytestbed.wifinodes:
            if node.wlan_ipAddress == remote_wlan_ipAddress and measurement != False:
                node.last_bunch_measurement.append(measurement)
                #log.debug('Append measurements at node %s : %s' % (str(remote_wlan_ipAddress), str(measurement) ))

    """
    Stop function used to send stop function to local controllers.
    """
    def stop_local_controller(mytestbed):
        CtrlFuncImpl = UPI_RN.stopFunc
        CtrlFuncargs =  {'INTERFACE' : ['wlan0']}
        now = get_now_full_second()
        # exec immediately
        exec_time = now + timedelta(seconds=3)
        log.info('Stop local WiSHFUL controller on all nodes - stop at : %s', str(exec_time))
        #nodes = upi_hc.getNodes()
        nodes = mytestbed.nodes
        try:
            callback = partial(resultCollector, funcId=99)
            mytestbed.global_mgr.runAt(nodes, UPI_RN.stopFunc, CtrlFuncargs, unix_time_as_tuple(exec_time), callback)
        except Exception as e:
            log.fatal("An error occurred when stop the local WiSHFUL controller: %s" % e)


    # START MAIN PART

    if disable:
        stop_local_controller(mytestbed)
        return

    # register callback function for collecting results
    mytestbed.global_mgr.setCtrlCollector(ctrlMsgCollector)
    # deploy a custom control program on each node
    CtrlFuncImpl = customLocalCtrlFunction
    CtrlFuncargs =  {'INTERFACE' : ['wlan0']}
    # get current time
    now = get_now_full_second()
    # exec immediately
    exec_time = now + timedelta(seconds=3)
    log.info('Sending local WiSHFUL controller on all nodes - start at : %s', str(exec_time))

    #nodes = upi_hc.getNodes()
    for node in mytestbed.wifinodes:
        node.measurement_types.append('FREEZING_NUMBER')
    nodes = mytestbed.nodes

    try:
        # this is a non-blocking call
        callback = partial(resultCollector, funcId=99)
        #isOntheflyReconfig = True
        mytestbed.global_mgr.runAt(nodes, CtrlFuncImpl, CtrlFuncargs, unix_time_as_tuple(exec_time), callback )
    except Exception as e:
        log.fatal("An error occurred in local controller WiSHFUL sending and running : %s" % e)

    log.info("Local logic STARTED")
    return


def programmable_callback(measurement_data):
    #log.debug("programmable callback is running")
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

    log.warning('*********** WISHFUL SC3 *************')
    log.warning('*********** starting global WiSHFUL controller **********************')

    """
    *********************
    Experiment Controller
    *********************
    We can swap this part with bash script or OML/OMF architecture
    """
    mytestbed = TestbedTopology("SC3",log)
    mytestbed.initializeTestbedTopology()       # discovery and allocate nodes
    mytestbed.initializeTestbedFunctions()      # set nodes rule: create network and association

    # serverApp0 = start_iperf_server_application(mytestbed.ap1, log, mytestbed)
    # time.sleep(1)
    # clientApp0 = start_iperf_client_application(mytestbed.sta1, mytestbed.ap1, log, mytestbed)
    # time.sleep(1)
    # clientApp1 = start_iperf_client_application(mytestbed.sta2, mytestbed.ap1, log, mytestbed)
    # time.sleep(1)
    # clientApp2 = start_iperf_client_application(mytestbed.sta3, mytestbed.ap1, log, mytestbed)
    #

    """
    *********************
    Wishful Controller
    *********************
    We implement here the controller logic to get measuerements and set node capabilities
    """

    """
    Start WiSHFUL controller measurement collector
    """
    meas_collector = MeasurementCollector(mytestbed, log)
    nodes_NIC_info = []
    for node in mytestbed.nodes:
        nodes_NIC_info.append(getPlatformInformation(node, log, mytestbed.global_mgr))


    seconds = 0
    while seconds < 5:
        log.debug('waiting for experiment controller end %d' % seconds)
        time.sleep(1)
        seconds += 1

    """
    Wishful ShowCase 3 PHASE 2
    """
    log.warning('***********             SHOWCASE 3 PHASE 2                **********************')
    log.warning('*********** All nodes are controlled by global controller **********************')

    """
    Set TDMA radio program on nodes
    """
    node_index = 0
    #superframesize in ms
    #superframe_size_len = 1060 * len(mytestbed.wifinodes)
    superframe_size_len = 700 * len(mytestbed.wifinodes)
    for node in mytestbed.nodes:

        active_TDMA_radio_program(node, log,mytestbed.global_mgr, nodes_NIC_info[node_index])

        tdma_params={'TDMA_SUPER_FRAME_SIZE' : superframe_size_len, 'TDMA_NUMBER_OF_SYNC_SLOT' : len(mytestbed.wifinodes), 'TDMA_ALLOCATED_SLOT': node_index}
        set_TDMA_parameters(node, log,mytestbed.global_mgr, tdma_params)

        node_index += 1

    seconds = 0
    while seconds < 15:
        log.debug('waiting for next TDMA setting %d' % seconds)
        time.sleep(1)
        seconds += 1

    """
    Start measurement collector for measure FREEZING_NUMBER on all nodes
    """
    #TODO get measurements
    #"""
    # measurements = (UPI_RN.TSF, UPI_RN.BUSY_TYME, UPI_RN.NUM_RX, UPI_RN.NUM_RX_MATCH, UPI_RN.NUM_TX)
    # measurements = (UPI_RN.TSF, UPI_RN.FREEZING_NUMBER)
    # my_reporting_period=2000000
    # my_iterations=60
    # meas_collector.collect_values_from_nodes(nodes=mytestbed.wifinodes, node_list=mytestbed.nodes, measurement_types=measurements,
    #                                          ucallback=programmable_callback, sampling_time=500000,
    #                                          reporting_period = my_reporting_period, iterations = my_iterations)
    #"""

    """
    Start traffic
    """
    serverApp0 = start_iperf_server_application(mytestbed.ap1, log, mytestbed)
    time.sleep(1)
    clientApp0 = start_iperf_client_application(mytestbed.sta1, mytestbed.ap1, log, mytestbed)
    time.sleep(1)
    clientApp1 = start_iperf_client_application(mytestbed.sta2, mytestbed.ap1, log, mytestbed)
    time.sleep(1)
    clientApp2 = start_iperf_client_application(mytestbed.sta3, mytestbed.ap1, log, mytestbed)

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

    #meas_collector.plot_last_measurements(nodes=mytestbed.wifinodes, measurement_types=['FREEZING_NUMBER'], plot_title="PLOT SC3 PHASE 1")

