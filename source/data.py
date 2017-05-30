"""
PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: April, 2017

Module containing classes which act as containers for
LEED and LEEM data sets. Each objects has a main data
construct consisting of a 3d numpy array which is filled
by reading in a stack of data files in either an image format
or raw binary data.

Alongside the 3d numpy array there must be some type of list or
container for energy parameters which corresponds directly to the
third axis of the numpy array.
"""


class LeedData(object):
    """Generic object to hold LEED Data and relevant variables."""

    def __init__(self, br=20):
        """Initialize LEEDData object."""
        self.dat3d = None  # placeholder for main data; overwritten on load
        self.elist = []  # list of energy values
        self.ilist = []
        self.data_dir = ''  # placeholder for path to currently stored data
        # Image settings will be set to appropriate values via the User inside gui.py
        self.ht = 0  # Height of image used in loading Raw data
        self.wd = 0  # Width of image used in loading Raw data
        self.box_rad = br  # default value is 20 yielding a 40x40 rectangular integration window
        self.average_ilist = None


class LeemData(object):
    """Generic object to hold LEEM data and relevant variables."""

    def __init__(self):
        """Initialize LEEDData object."""
        # Image Parameters
        self.ht = 0  # image height to be set by User
        self.wd = 0  # image width to be set by User
        self.hdln = 0  # image header length to be set by User
        # Data
        self.dat3d = None  # placeholder for main data; overwritten on load
        self.elist = []  # list of energy values
        self.ilist = []
        self.e_step = 0
        # Directories and Image index
        self.data_dir = ''
        self.img_mask_count_dir = ''
        self.curimg = 0  # correspondent to third axis of self.dat3d
        # Coordinates for I(V) data
        self.curX = 0
        self.curY = 0
        self.timelist = []  # used for plotting I(t) data
