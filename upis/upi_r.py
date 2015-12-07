__author__ = 'pruckebusch'

import abc
#~ from upis.upi_n import UPI_N

"""
EU project WISHFUL

The WISHFUL interface definitions - UPIs (UPI_R/UPI_N) for device control.

The interface between the local control program and the Wishful engine.
"""

class NIC_t:
    """
    Class to identify network interfaced cards
    """
    interface = ""
    platform = ""

class radio_info_t:
	"""
	Class to save radio specific
	"""
	NIC_info = None

	event_list = []
	monitor_list = []
	param_list = []

"""
The UPI_R - UPI for radio control at device level.
"""
class UPI_R(object):
	__metaclass__ = abc.ABCMeta

	""" Generic functions for configuration
	"""

	"""
	Supported parameters
	"""
	# get/set rf channel on a wireless network interface
	IEEE80211_CHANNEL = "IEEE80211_CHANNEL"
	# get MAC address of network interface card
	NETWORK_INTERFACE_HW_ADDRESS = "NETWORK_INTERFACE_HW_ADDRESS"
	# measure the transmit rate of generated 802.11 broadcast traffic at full rate
	IEEE80211_L2_BCAST_TRANSMIT_RATE = "IEEE80211_L2_BCAST_TRANSMIT_RATE"
	# send out 802.11 broadcast link probes
	IEEE80211_L2_GEN_LINK_PROBING = "IEEE80211_L2_GEN_LINK_PROBING"
	# receive 802.11 broadcast link probes
	IEEE80211_L2_SNIFF_LINK_PROBING = "IEEE80211_L2_SNIFF_LINK_PROBING"
	#connect to ap
	IEEE80211_CONNECT_TO_AP = "IEEE80211_CONNECT_TO_AP"
	
	IEEE_802154_CHANNEL = "IEEE_802154_CHANNEL"
	IEEE_802154_PANID = "IEEE_802154_PANID"
	IEEE_802154_SHORTADDR = "IEEE_802154_SHORTADDR"
	IEEE_802154_MINBE = "IEEE_802154_MINBE"
	IEEE_802154_MAXBE = "IEEE_802154_MAXBE"
	IEEE_802154E_SLOTFRAME = "IEEE_802154E_SLOTFRAME"
	IEEE_802154E_SLOTFRAMELENGTH = "IEEE_802154E_SLOTFRAMELENGTH"
	TAISC_ACTIVERADIOPROGRAM = "TAISC_ACTIVERADIOPROGRAM"
	IEEE_802154E_CHANNELHOPPINGSEQ = "IEEE_802154E_CHANNELHOPPINGSEQ"
	IEEE_802154_CHANNELHOPPINGSEQLENGTH = "IEEE_802154_CHANNELHOPPINGSEQLENGTH"

	#PHY PARAMETERS
	#not implemented
	IEEE80211_AP_CHANNEL = "IEEE80211_AP_CHANNEL"
	IEEE80211_CHANNEL = "IEEE80211_CHANNEL"
	IEEE80211_MCS = "IEEE80211_MCS"
	IEEE80211_CCA = "IEEE80211_CCA"
	TX_POWER = "TX_POWER"
	TX_ANTENNA = "TX_ANTENNA"
	RX_ANTENNA = "RX_ANTENNA"

	#Used to set the Access Point MAC address to get the synchronization TSF timer
	MAC_ADDR_SYNCHRONIZATION_AP = "MAC_ADDR_SYNCHRONIZATION_AP"

	#*****************************
	#TDMA RADIO PROGRAM PARAMETERS
	#use setParameterLowerLayer to set value
	#use getParameterLowerLayer to get value
	#*****************************
	#implemented
	TDMA_SUPER_FRAME_SIZE = "TDMA_SUPER_FRAME_SIZE"
	TDMA_NUMBER_OF_SYNC_SLOT = "TDMA_NUMBER_OF_SYNC_SLOT"
	TDMA_ALLOCATED_SLOT = "TDMA_ALLOCATED_SLOT"

	#not implemented
	TDMA_MAC_PRIORITY_CLASS = "TDMA_MAC_PRIORITY_CLASS"

	#*****************************
	#CSMA RADIO PROGRAM PARAMETERS
	#use setParameterLowerLayer to set value
	#use getParameterLowerLayer to get value
	#*****************************

	#implemented
	CSMA_CW = "CSMA_CW"
	CSMA_CW_MIN = "CSMA_CW_MIN"
	CSMA_CW_MAX = "CSMA_CW_MAX"

	#not implemented
	CSMA_TIMESLOT = "CSMA_TIMESLOT"
	CSMA_MAC_PRIORITY_CLASS = "CSMA_MAC_PRIORITY_CLASS"
	CSMA_BACKOFF_VALUE = "CSMA_BACKOFF_VALUE"


	#*****************************
	#RADIO MEASURAMENT
	#use getMonitor to get measurament value
	#*****************************

	#implemented
	NUM_TX = "NUM_TX"
	NUM_TX_UNIT = "samples"
	NUM_TX_SUCCESS = "NUM_TX_SUCCESS"
	NUM_TX_SUCCESS_UNIT = "samples"

	NUM_RX = "NUM_RX"
	NUM_RX_UNIT = "samples"
	NUM_RX_SUCCESS = "NUM_RX_SUCCESS"
	NUM_RX_SUCCESS_UNIT = "samples"
	NUM_RX_MATCH = "NUM_RX_MATCH"
	NUM_RX_MATCH_UNIT = "samples"

	BUSY_TYME = "BUSY_TIME"             #microsecond from association 32bit (cycle on 4294 sec)
	BUSY_TYME_UNIT = "us"             #microsecond from association 32bit (cycle on 4294 sec)

	NUM_FREEZING_COUNT = "NUM_FREEZING_COUNT"
	NUM_FREEZING_COUNT_UNIT = "samples"

	TX_ACTIVITY = "TX_ACTIVITY"
	TX_ACTIVITY_UNIT = "us"

	TSF = "TSF"
	TSF_UNIT = "us"

	@abc.abstractmethod
	def getNICs(self):
		"""Get the list of available interface names and platforms (TAISC, WMP, ATHxK) running on each interface.
		
		:returns: A list of available NICs.
		:rtype: upi_r.NIC_t
		"""
		return

	@abc.abstractmethod
	def getNICInfo(self, nic):
		"""Get the radio capabilities of a given network card NIC_t in terms of event, measurement and parameter lists
		
		:param nic: The NIC specifier.
		:type nic: upi_r.NIC_t
		:returns: A RadioInfo object containing the list of events, measurements and parameters.
		:rtype: upi_r.radio_info_t
		"""
		return

	@abc.abstractmethod
	def setParameterLowerLayer(self, iface, param_key_value):
		"""Set one (or more) parameter(s) on radio / lower MAC.
		
		:param iface: The name of the interface.
		:type iface: str.
		:param param_key_value: Dictionary containing the key(s) and value(s) of the parameter(s) {'key1':value1, 'key2':value2, ...}.
		:type param_key_value: dict.
		:returns: Dictionary containing the key(s) and return code(s) {'key1':ret1, 'key2':ret2, ...}.
		"""
		return

	@abc.abstractmethod
	def getParameterLowerLayer(self, iface, param_key):
		"""Get one (or more) parameter(s) on on radio / lower MAC.
		
		:param iface: The name of the interface.
		:type iface: str.
		:param param_key: a list of parameter keys ['key1','key2',...].
		:type param_key: list.
		:returns: Dictionary containing the key(s) and values(s) for the requested parameter(s) {'key1':value1, 'key2':value2, ...}.
		"""
		return

	@abc.abstractmethod
	def getMonitor(self, iface, param_key):
		"""Get one (or more) monitoring value(s) on radio / lower MAC
		
		:param string iface: name of the interface
		:param list param_key: monitoring parameter keys ['key1','key2',...]
		:returns: A Dictionary with the key(s) and value(s) of the monitor parameter(s) {'key1':value1, 'key2':value2, ...}
		"""
		return

	@abc.abstractmethod
	def getActive(self, iface):
		"""Get active radio program from a particular interface.
		
		:param string iface: name of the interface.
		:returns: string. The name of the Active Radio Program
		"""
		return

	@abc.abstractmethod
	def inject(self, iface, radioProgramName):
		"""Inject radio program on a particular interface.
		
		:param string iface: name of the interface.
		:param string radioProgramName: name of the RadioProgram (ATH9K_HYBRIDMAC, CSMA, TDMA).
		:returns:
			bool.  The return code::

				True -- Success!
				False -- No good.
		"""
		return

	@abc.abstractmethod
	def setActive(self, iface, radioProgramName, init_param_key_value):
		""" Allows to configure the enhanced distributed channel access parameters on a specific interface and queue.
		
		:param string iface: name of the interface.
		:param string radioProgramName: name of the RadioProgram (ATH9K_HYBRIDMAC, CSMA, TDMA).
		:param dict init_param_key_value: Dictionary containing the key(s) and values(s) for the init parameter(s) {'key1':value1, 'key2':value2, ...} of the Radio Program.
		:returns:
			bool.  The return code::

				True -- Success!
				False -- No good.
		"""
		return
	
	@abc.abstractmethod
	def setInActive(self, iface, radioProgramName):
		""" Allows to configure the enhanced distributed channel access parameters on a specific interface and queue.
		
		:param string iface: name of the interface.
		:param string radioProgramName: name of the RadioProgram (ATH9K_HYBRIDMAC, CSMA, TDMA).
		:param dict init_param_key_value: Dictionary containing the key(s) and values(s) for the init parameter(s) {'key1':value1, 'key2':value2, ...} of the Radio Program.
		:returns:
			bool.  The return code::

				True -- Success!
				False -- No good.
		"""
		return
	
	@abc.abstractmethod
	def setEdcaParameters(self, iface, queueId, edcaparam_key_value):
		""" Allows to configure the enhanced distributed channel access parameters (aifs, cwmin, cwmax, txop) on a specific hardware queue in a specific interface.
		
		:param string iface: name of the interface.
		:param int queueId: ID of the hardware QUEUE.
		:param dict edcaparam_key_value: EDCA parameters key value pairs
				{'aifs':0-255, 'cwmin':1-1023, 'cwmax':1-1023, 'txop':0-999}. 
		:returns:
			bool.  The return code::

				True -- Success!
				False -- Fail!
		"""
		return

	@abc.abstractmethod
	def getEdcaParameters(self, iface, queueId):
		""" Allows to obtain the enhanced distributed channel access parameters (aifs, cwmin, cwmax, txop) used on a specific hardware queue in a specific interface.
		
		:param string iface: name of the interface.
		:param int queueId: ID of the hardware QUEUE.
		:returns:
			Dictionary.  EDCA parameters key value pairs::

				{'aifs':0-255, 'cwmin':1-1023, 'cwmax':1-1023, 'txop':0-999}
		"""
		return

	@abc.abstractmethod
	def setPerFlowTxPower(self, iface, flow, txPower):
		""" Allows to set a TX power per flow.
		
		:param: iface: name of the interface.
		:type  iface: string
		:param flow: Flow descriptor.
		:type flow: :py:class:`pytc.Filter.FlowDesc`
		:returns: The return code.
		:rtype: bool
		
		"""
		return

	@abc.abstractmethod
	def cleanPerFlowTxPowerList(self, iface):
		""" Removes the TX power settings for all flows.
		
		:param iface: name of the interface.
		:type iface: string.
		:returns:
			bool.  The return code::

				True -- Success!
				False -- Fail!
		
		"""
		return

	@abc.abstractmethod
	def getPerFlowTxPowerList(self, iface):
		""" Returns the TX power set per flow on an interface.
		
		:param iface: name of the interface.
		:type iface: string.
		:returns: Dict.  A dictionary with as keys the flows(pytc.Filter.FlowDesc) and values the TX power.
		"""
		return

	@abc.abstractmethod
	def genBacklogged80211L2BcastTraffic(self, iface, num_packets, ipPayloadSize, phyBroadcastMbps, ipdst, ipsrc, use_tcpreplay):
		""" Sends as fast as possible L2 broadcast traffic. Note that all transmitted packets are identical.
		
		:param string iface: name of the interface.
		:param int num_packets:
		:param int ipPayloadSize:
		:param int phyBroadcastMbps:
		:param string ipdst:
		:param string ipsrc:
		:param bool use_tcpreplay:
		:returns: float.  The achieved transmit frame rate.
		"""
		return

	@abc.abstractmethod
	def getHwAddr(self, iface):
		""" Returns the Hardware address of the specified interface.
		
		:param string iface: name of the interface.
		:returns: string.  The hardware address.
		"""
		return

	@abc.abstractmethod
	def setRfChannel(self, iface, channel):
		""" Sets the RF channel on the specified interface.
		
		:param string iface: name of the interface.
		:param int channel: the channel number.
		:returns:
			bool.  The return code::

				True -- Success!
				False -- Fail!
		"""
		return

#~ class UPI_RN(UPI_R, UPI_N):
	#~ __metaclass__ = abc.ABCMeta
#~ 
	#~ @abc.abstractmethod
	#~ def stopFunc(self):
		#~ """Helper to stop execution of local controller
		#~ """
		#~ return
