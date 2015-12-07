__author__ = 'A. Zubow'

import abc

"""
EU project WISHFUL

The WISHFUL interface definitions for execution of global Network Functions (NF) defined on UPI_G interface.
"""

class UPI_G(object):
    __metaclass__ = abc.ABCMeta

    """
    Supported global NFs
    """

    # NF used to find for each pair of network nodes whether they are in carrier sensing range or not
    NF_GET_NODES_IN_CARRIERSENSING_RANGE = "NF_GET_NODES_IN_CARRIERSENSING_RANGE"
    # NF used to find for each pair of network nodes whether they are in communication range or not
    NF_GET_NODES_IN_COMMUNICATION_RANGE = "NF_GET_NODES_IN_COMMUNICATION_RANGE"
    # NF used to get link transmission parameters between two nodes 
    NF_GET_LINK_PARAMETERS = "NF_GET_LINK_PARAMETERS"

    @abc.abstractmethod
    def execNetworkFunction(self, nf_key_value):
        """Execute a network function in the network
        :param nf_key_value: key and value of the NF to be executed
        """
        return

    @abc.abstractmethod
    def getNodes(self, customFilter):
        """Retrieve all nodes which can be controlled
        :param string customfilter: optional filter.
        
        """
        return

    """ Remote execution of node-level function """
    @abc.abstractmethod
    def runAt(self, node_lst, UPIfunc, UPIargs, exec_time, resultCallbackfunc=None, priority=1):
        """Exec remote function on UPI_R/N
        :param node_lst: list of nodes we want to exec function
        :param UPIfunc: UPI (R/N) function to be executed
        :param UPIargs: UPI function arguments
        :param exec_time: absolute time since epoch (2-tuple of second & microsecond) when the function will be executed or None for immediate execution
        :param resultCallbackfunc: the callback used for returning results of time scheduled function execution.
        :param priority: as in UNIX, lower priority numbers mean higher priority
        """
        return

    @abc.abstractmethod
    def stopAt(self, node_lst, exec_time, resultCallbackfunc=None):
        """Used to stop remote functions, e.g. loops
        :param node_lst: list of nodes we want to exec function
        :param exec_time: absolute time when the function will be executed or -1 for immediate execution
        :param resultCallbackfunc: the callback used for returning results of time scheduled function execution.
        """
        return

    """ Execution of network-level function """
    @abc.abstractmethod
    def runNFAt(self, UPIfunc, UPIargs, exec_time, resultCallbackfunc=None, priority=1):
        """Exec global functions on UPI_G
        :param UPIfunc: UPI_G function to be executed
        :param UPIargs: UPI function arguments
        :param exec_time: absolute time since epoch (2-tuple of second & microsecond) when the function will be executed or None for immediate execution
        :param resultCallbackfunc: the callback used for returning results of time scheduled function execution.
        :param priority: as in UNIX, lower priority numbers mean higher priority
        """
        return
