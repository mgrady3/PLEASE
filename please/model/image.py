""" This module contains an implementation of the base IEMImage class, used
to represent Electron Microscopy image data for common formats such as
LEEM/LEED data.
"""

from .interfaces import IEMImage
from please.io.readers import read_image_data


class EMImage(IEMImage):
    @classmethod
    def from_file(cls, path):
        """ Get an EMImage from file

        Parameters
        ----------
        path : str
            String indicating the absolute path to data file to load image
            data from
        """
        return cls(data=read_image_data(path))
