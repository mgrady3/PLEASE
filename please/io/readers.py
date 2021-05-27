""" This module contains I/O code for reading data from supported formats
such as raw .dat files as well as common image types like TIFF and PNG.
"""
import pathlib

import numpy as np
from PIL import Image

from please.constants import (
    SUPPORTED_IMAGE_FORMATS, SUPPORTED_RAW_FORMATS,
)
from please.constants import BITS_PER_BYTE
from please.exceptions import UnsupportedDataType



def read_image_data(file_path: str) -> np.ndarray:
    """ Generate a 2d numpy of image data from an image file

    Parameters
    ----------
    file_path : str
        Path to the image file to read into a numpy array

    Returns
    -------
    data : NDArray
        2D array of image data
    """
    ext = pathlib.Path(file_path).suffix
    if ext:
        try:
            ext = ext.split('.')[1].upper()
        except IndexError:
            pass
    if not ext in SUPPORTED_IMAGE_FORMATS:
        raise UnsupportedDataType(
            f'The file, {file_path}, could not be loaded because the data format'
            ' is not supported.'
        )

    return np.array(Image.open(file_path).convert('L'))


def read_raw_data(
        file_path: str,
        height: int,
        width: int,
        bits_per_pixel: int,
        byteorder: str
    ) -> np.ndarray:
    """ Generate a 2d numpy of image data from a raw data (.dat) file

    Parameters
    ----------
    file_path : str
        Path to the data file to read into a numpy array

    Returns
    -------
    data : NDArray
        2D array of image data

    Notes
    -----
    This function performs a "dumb" parse of the file to extract the image
    data. It requires knowledge of the expected image characteristics, namely
    height, width, bits per pixel, and byte ordering i.e. endianness. With this
    knowledge, the header can be safely discarded and only the image data
    retained.
    """
    if bits_per_pixel % BITS_PER_BYTE != 0:
        raise ValueError(
            f"Unsupported bit-depth: {bits_per_pixel}."
            f" Must be positive integer multiple of {BITS_PER_BYTE}."
        )
    ext = pathlib.Path(file_path).suffix
    if ext:
        try:
            ext = ext.split('.')[1].upper()
        except IndexError:
            pass
    if not ext in SUPPORTED_RAW_FORMATS:
        raise UnsupportedDataType(
            f'The file, {file_path}, could not be loaded because the data format'
            ' is not supported.'
        )

    # Extract the image data from the file contents
    with open(file_path, 'rb') as f:
        file_data = f.read()

    file_length_in_bytes = len(file_data)
    image_data_in_bytes = height * width * int(bits_per_pixel/BITS_PER_BYTE)
    header_length_in_bytes = file_length_in_bytes - image_data_in_bytes
    if header_length_in_bytes < 0:
        raise ValueError(
            f"Can not read raw data file, {file_path}."
            " Image parameters do not match the data file."
        )
    image_data = file_data[header_length_in_bytes:]
    format_string = _get_dtype_string(bits_per_pixel, byteorder)
    return np.frombuffer(image_data, format_string).reshape((height, width))


def _get_dtype_string(bits: int, byteorder: str) -> str:
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