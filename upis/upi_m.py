__author__ = 'D. Garlisi'

"""
EU project WISHFUL
"""

import abc

"""
The WISHFUL interface definitions - UPIs (UPI_M) for install/update/active/deactive software modules.
"""

"""
The UPI_M - UPI for managing protocol software modules at any layer.
"""
class UPI_M(object):
    __metaclass__ = abc.ABCMeta

    """ Generic functions for configuration
    """

    @abc.abstractmethod
    def installExecutionEngine(self, param_key):
        """Set the ...
        :param
        type ...
        path ...
        :return result
        """
        return

    @abc.abstractmethod
    def initTest(self, param_key):
        """Activate the
        :param type ...
        :return result
        """
        return
