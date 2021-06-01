""" This module contains custom exceptions that may be raised during I/O
tasks such as attempting to read data from disk.
"""


class PLEASEIOError(Exception):
    """ Base class for I/O error in the PLEASE application code """
    pass


class UnsupportedDataType(PLEASEIOError):
    """ Error due to attempt to load an unsupported data format """
    pass
