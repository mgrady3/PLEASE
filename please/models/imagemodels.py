"""
Classes modeling electron microscope image data
"""

import numpy as np
from traits.api import (
    Array, ArrayOrNone, Either, File, Float, HasTraits, Int, Interface,
    Instance, Property, Unicode, provides
)

from please.io.imageio import _get_arrary_from_file


class IEMImage(Interface):
    """Interface for one of many Electron Microscope image types:
    e.g. LEEM, LEED, PEEM
    """

    #: A 2D numpy array representing an EM image
    data = Property(Array)

    #: Absolute path to the data file
    data_path = File()

    #: Height of image in pixels
    height = Int()

    #: Width of image in pixels
    width = Int()


@provides(IEMImage)
class EMImage(HasTraits):
    """Representation of an Electron Microscope image

    Data array is lazily loaded from file on request
    """
    #: A 2D numpy array representing an EM image in (row, col) shape
    data = Property(Array)

    #: Absolute path to the data file. Can be none if data not loaded from file
    data_path = Either(File, None)

    #: Height of image in pixels
    height = Int()

    #: Width of image in pixels
    width = Int()

    @cached_property
    def get_data(self):
        """Get the data of an image from file."""
        return _get_arrary_from_file(self.data_path)

    def set_data(self, new_array):
        """Set the data of the image to a new array and update shape.

        This allows loading image data from another source rather than from
        file.
        """
        self.data = new_array
        self.height, self.width = new_array.shape


class IEMImageStack(Interface):
    """Interface for a stack of Electron Microscopy images representing a
    collective data set such as a spectroscopic data set.
    """
    #: Current image of the stack being viewed or manipulated as an ImageModel
    current_image = Property(Instance(IEMImage))

    #: Full 3D numpy array with images represented as (row, column)
    #: And the third (depth) axis representing the spectroscopic nature
    data = Property(Array)

    #: SI unit used for the values recorded in depth_values
    depth_unit = Unicode()

    #: The 3rd axis of the image stack should have a 1:1 mapping to an external
    #: measurement or setting. For instance, an I(V) data set constitutes a set
    #: of images as a function of Energy (represented by an accelerating
    #: voltage). Other common values would be time or temperature
    depth_values = List(Float)

    #: Number of images in the stack.
    # Must always equal data.shape[2] and len(depth_values)
    num_images = Int

