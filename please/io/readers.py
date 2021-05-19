""" This module contains I/O code for reading data from supported formats
such as raw .dat files as well as common image types like TIFF and PNG.
"""

import pathlib

import numpy as np
from PIL import Image

from please.constants import (
    SUPPORTED_IMAGE_FORMATS, SUPPORTED_RAW_FORMATS,
)
from please.exceptions import UnsupportedDataType


def read_image_data(path):
    """ Load image data from the specified file path to a numpy array

    Parameters
    ----------
    path : str
        String indicating the absolute file path to open

    Returns
    -------
    data : numpy.NDArray

    Notes
    -----
    This function acts as a dispatcher to the appropriate laoder based on
    the detected file type
    """
    ext = pathlib.Path(path).suffix
    if ext:
        try:
            ext = ext.split('.')[1].upper()
        except IndexError:
            pass
    if not ext in SUPPORTED_IMAGE_FORMATS + SUPPORTED_RAW_FORMATS:
        raise UnsupportedDataType(
            f'The file, {path}, could not be loaded because the data format'
            ' is not supported.'
        )

    if ext in SUPPORTED_RAW_FORMATS:
        return _load_image_data_from_raw(path)
    else:
        return _load_image_data_from_image(path)


# TODO: re-implement I/O for raw files
def _load_image_data_from_raw(path):
    """ Load image data from a raw .dat file

    Parameters
    ----------
    path : str
        String indicating the absolute file path to open

    Returns
    -------
    data : numpy.NDArray
    """
    pass


def _load_image_data_from_image(path):
    """ Load image data from an image file

    Parameters
    ----------
    path : str
        String indicating the absolute file path to open

    Returns
    -------
    data : numpy.NDArray
    """
    return np.array(Image.open(path).convert('L'))
