__author__ = 'pruckebusch'

import abc
#~ from upis.upi_r import UPI_R

"""
EU project WISHFUL

The WISHFUL interface definitions - UPIs (UPI_R/UPI_N) for device control.

The interface between the local control program and the Wishful engine.
"""


"""
The UPI_N - UPI for controlling the network stack at the device level.
"""
class UPI_N(object):
    __metaclass__ = abc.ABCMeta

    """ Generic functions for configuration
    """

    """ higher MAC """
    # get IP address of a network interface
    IFACE_IP_ADDR = "IFACE_IP_ADDR"

    @abc.abstractmethod
    def setParameterHigherLayer(self, iface, param_key_value):
        """Set the parameter on higher layers of protocol stack (higher MAC and above)
        :param iface (string): string name of the interface
        :param param_key_value (dictonary): key and value of the parameters {'key1':value1, 'key2':value2, ...}
        :return for each parameter the success 
        """
        return

    @abc.abstractmethod
    def getParameterHigherLayer(self, iface, param_key):
        """Get one or more parameters on higher layers of protocol stack (higher MAC and above)
        :param iface (string): string name of the interface
        :param param_key (list): a list of list of parameter keys ['key1','key2',...]
        :return key_value (dictionary): the key and value of the parameters {'key1':value1, 'key2':value2, ...}
        """
        return

    @abc.abstractmethod
    def startIperfServer(self, iface, serverPort):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def startIperfClient(self, iface, serverIP, serverPort, period):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def startPing(self, iface, srcAddress, dstAddres):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def setProfile(self, iface, profile):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def updateProfile(self, iface, profile):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def removeProfile(self, iface, profile):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def setPerLinkProfile(self, iface, srcNode, dstNode, profile):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def updatePerLinkProfile(self, iface, srcNode, dstNode, profile):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def removePerLinkProfile(self, iface, srcNode, dstNode):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def installEgressScheduler(self, iface, scheduler):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def removeEgressScheduler(self, iface):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def clearIpTables(self, table, chain):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def getIpTable(self, table, chain):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def setMarking(self, flowDesc, markId, table, chain):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def delMarking(self, flowDesc, markId, table, chain):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def setTos(self, flowDesc, tos, table, chain):
        """
        Func Desc
        """
        return

    @abc.abstractmethod
    def delTos(self, flowDesc, tos, table, chain):
        """
        Func Desc
        """
        return

    #~ @abc.abstractmethod
    #~ def installApplication(self, param_key):
        #~ """
        #~ Func Desc
        #~ """
        #~ return

#~ class UPI_RN(UPI_R, UPI_N):
    #~ __metaclass__ = abc.ABCMeta
#~ 
    #~ @abc.abstractmethod
    #~ def stopFunc(self):
        #~ """Helper to stop execution of local controller
        #~ """
        #~ return
