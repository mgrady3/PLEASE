""" This module contains helper functions for common tasks encountered during
image/data file I/O
"""

import pathlib

from please.constants import SUPPORTED_IMAGE_FORMATS, SUPPORTED_RAW_FORMATS


def get_file_extension(path: str) -> str:
    """ Get the extension of an image/data file

    Parameters
    ----------
    path : str
        String indicating path to the file

    Returns
    -------
    ext : str
        Extension of the file
    """
    return pathlib.Path(path).suffix


def is_image_file(path: str) -> bool:
    """ Is the file at the specified path a supported image type? """
    ext = get_file_extension(path).upper()
    return ext.strip('.') in SUPPORTED_IMAGE_FORMATS


def is_raw_file(path: str) -> bool:
    """ Is the file at the specified path a supported raw data type? """
    ext = get_file_extension(path).upper()
    return ext.strip('.') in SUPPORTED_RAW_FORMATS
