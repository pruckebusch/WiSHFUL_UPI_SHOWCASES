__author__ = 'A. Zubow'

import abc
from upis.upi_r import UPI_R
from upis.upi_n import UPI_N

"""
EU project WISHFUL

The WISHFUL interface definitions - UPIs (UPI_R/UPI_N) for device control.

The interface between the local control program and the Wishful engine.
"""

"""
The UPI_L - UPI for local control at device level.
"""
class UPI_L(UPI_R, UPI_N):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def stopFunc(self):
        """Helper to stop execution of local controller
        """
        return
