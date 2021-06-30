""" This module contains I/O code for reading data from supported formats
such as raw .dat files as well as common image types like TIFF and PNG.
"""
import pathlib
import struct

import numpy as np
from PIL import Image

from please.constants import (
    SUPPORTED_IMAGE_FORMATS, SUPPORTED_RAW_FORMATS,
)
from please.constants import BITS_PER_BYTE
from please.exceptions import UnsupportedDataType
from please.io.utils import get_dtype_string, is_uview

# How many bytes to read for each variable stored in the file header
# Note: This is subject to change in future versions of UView
UK_ID_LEN = 20
UK_SIZE_LEN = 2
UK_VERSION_LEN = 2
BITS_PER_PIXEL = 2
START_TIME = 8
IMAGE_WDITH = 2
IMAGE_HEIGHT = 2
NUM_IMAGES = 2
ALIGNMENT = 6


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
    if ext not in SUPPORTED_IMAGE_FORMATS:
        raise UnsupportedDataType(
            f'The file, {file_path}, could not be loaded because the data'
            ' format is not supported.'
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

    height : int
        Image height in pixels

    width : int
        Image width in pixels

    bits_per_pixel : int
        Number of bits of file data for each pixel

    byteorder : str
        String indicating the byte ordering of the data, 'L' for little endian
        or 'B' for big endian. Generally files will be 'L', however, some
        outliers will be 'B'.

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
    if ext not in SUPPORTED_RAW_FORMATS:
        raise UnsupportedDataType(
            f'The file, {file_path}, could not be loaded because the data'
            ' format is not supported.'
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
    format_string = get_dtype_string(bits_per_pixel, byteorder)
    return np.frombuffer(image_data, format_string).reshape((height, width))


def read_uview(file_path: str, byteorder: str = 'L') -> np.ndarray:
    """ Attempt to read a UView (UKSOFT2001) image data file into a 2D numpy
    array containing the image contents by parsing the file header using
    known structure of the header contents

    Parameters
    ----------
    file_path : str
        Path to the file to read into an array

    byteorder : str, optional

    Returns
    -------
    2D numpy array containing raw image data

    Raises
    ------
    UnsupportedDataType

    Notes
    -----
    This function performs a "smart" parse of the file based on quasi known
    structure of the file header. Various versions of UView have slightly
    differing header contents. Here only a minimal set of required data is
    parsed from the header to avoid more complex parsing based on different
    versions.
    """
    if not is_uview(file_path):
        raise UnsupportedDataType(
            f"The file, {file_path} is not a valid UView data file."
        )
    with open(file_path, 'rb') as f:
        try:
            uk_id = struct.unpack(f'{UK_ID_LEN}s', f.read(UK_ID_LEN))[0]
            uk_size = struct.unpack('h', f.read(UK_SIZE_LEN))[0]
            uk_version = struct.unpack('h', f.read(UK_VERSION_LEN))[0]
            bits_per_pixel = struct.unpack('h', f.read(BITS_PER_PIXEL))[0]
            # Skip the next 6 bytes as they are unused space for alignment
            f.read(ALIGNMENT)
            start_time = struct.unpack('q', f.read(START_TIME))[0]
            img_width = struct.unpack('h', f.read(IMAGE_WDITH))[0]
            img_height = struct.unpack('h', f.read(IMAGE_HEIGHT))[0]
            num_images = struct.unpack('h', f.read(NUM_IMAGES))[0]
        except struct.error:
            raise UnsupportedDataType("Could not read UView header.")

        if num_images > 1:
            # TODO: Figure out a way to unpack each image
            raise UnsupportedDataType("Can not read multi-image file.")

        # Now we have all the information needed to extract the image
        # data from the file. We extract the image data from the end of the
        # file as follows:
        f.seek(0)
        num_pixels = img_width * img_height
        img_data_length_in_bytes = num_pixels * bits_per_pixel // BITS_PER_BYTE
        all_data = f.read()

    if len(all_data) < img_data_length_in_bytes:
        raise UnsupportedDataType("Not enough data. Possibly compressed.")
    header_len = len(all_data) - img_data_length_in_bytes

    # Extract just the image section, discarding the header
    img_data = all_data[header_len:]
    format_string = get_dtype_string(bits_per_pixel, byteorder)
    img_array = np.frombuffer(img_data, format_string)
    return img_array.reshape((img_height, img_width))
