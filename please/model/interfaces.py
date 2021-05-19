""" This module defines base classes to represent Electron Microscope data and
experiments concering various EM data
"""

from traits.api import (
    ABCHasStrictTraits, Array, Enum, Int, Property, Str, Tuple,
)

from please.constants import (
    ENDIAN_STRINGS, EXTERNAL_PARAMETERS, SUPPORTED_DATA_TYPES,
    SUPPORTED_EXPERIMENT_TYPES,
)


class IEMImage(ABCHasStrictTraits):
    """ Interface for an Electron Microscope Image Model """

    #: Image height in pixels
    height = Property(Int, depends_on='shape')

    #: Image width in pixels
    width = Property(Int, depends_on='shape')

    # Tuple defining data shape in (height, width) format
    shape = Property(Tuple(Int, Int), depends_on='data')

    #: Numpy-like Array of Image data with shape (height, width)
    data = Array(shape=(None, None))

    def _get_shape(self):
        """ Get the image shape in (height, width) format. """
        return self.data.shape

    def _get_height(self):
        """ Get the image height in pixels. """
        return self.shape[0]

    def _get_width(self):
        """ Get the image width in pixels. """
        return self.shape[1]


class IEMExperiment(ABCHasStrictTraits):
    """ Interface definition for an Electron Microscope Experiment.

    Whereas the IEMImage model provides an interface for a single electron
    microscope image object, the IEMExperiment interface represents a
    collection of Electron Microscope images coupled with one or more
    external paramters. Together this collection of data represents a
    spectroscopic data set.

    Examples
    --------
    A stack of Electron Microscope images collected from the same sample region
    each at a different value of incident electron Energy, parameterized by
    the voltage, V, forms an I(V) data set. Here the data of interest is how
    the image intensity, I, changes as a function of the external parameter, V.
    """

    #: Name identifying this experiment
    name = Str

    #: String indicating the type of this experiment
    #: See please.constants.SUPPORTED_DATA_TYPES
    #: Default: 'LEEM'
    experiment_type = Enum('LEEM', SUPPORTED_EXPERIMENT_TYPES)

    #: String indicating the type of data for this experiment
    data_type = Enum('RAW', SUPPORTED_DATA_TYPES)

    #: String indicating the file extension for the data for this experiment
    file_format = Str

    #: String indicating the absolute path to the directory containing data
    data_path = Str

    #: Integer indicating the number of bits per pixel in each data file
    bit_size = Int

    #: String indicating the byte-ordering for data for this experiment
    byte_order = Enum('L', ENDIAN_STRINGS)

    #: Tuple of integers indicating the height, width for each image
    image_parameters = Tuple()

    #: External parameter defining the fundamental relationship for this data
    external_parameter_name = Enum('Energy', EXTERNAL_PARAMETERS)

    #: Numeric data for external parameter
    external_parameter = Array()
