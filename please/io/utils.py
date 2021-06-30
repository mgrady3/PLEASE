""" This module contains helper functions for common tasks encountered during
image/data file I/O
"""

import pathlib

from please.constants import SUPPORTED_IMAGE_FORMATS, SUPPORTED_RAW_FORMATS


UVIEW_MAGIC = b'UKSOFT2001'  # magic bytes for UView image files


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


def get_dtype_string(bits: int, byteorder: str) -> str:
    """ Generate a numpy compatable string indicating the array dtype

    Parameters
    ----------
    bits : int
        Number of bits per pixel in the image data

    byteorder: str
        String indicating endianness, "L" for little-endian, "B" for big.

    Returns
    -------
    format_string : str
        numpy compatable dtype string for formatting image data
    """
    if bits not in {8, 16}:
        raise ValueError(f"Unsupported bit size: {bits}.")
    if byteorder not in {'L', 'B'}:
        raise ValueError(f"Unsupported byteorder: {byteorder}.")
    endian = '<' if byteorder == 'L' else '>'
    bitstring = 'u1' if bits == 8 else 'u2'
    return endian + bitstring


def is_uview(path: str) -> bool:
    """ Is the file at the specified path a UView data file? """
    with open(path,  'rb') as f:
        magic_bytes = f.read(len(UVIEW_MAGIC))
    return magic_bytes == UVIEW_MAGIC
