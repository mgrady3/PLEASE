""" This module contains constants used by various model code
"""

# TODO: add support for ARPES data and potentially other types
# See GH Issue: #11
SUPPORTED_EXPERIMENT_TYPES = {
    'LEEM',
    'LEED',
}

SUPPORTED_DATA_TYPES = {
    'Image',
    'Raw',
}

SUPPORTED_IMAGE_FORMATS = {
    'PNG',
    'TIFF',
}

SUPPORTED_RAW_FORMATS = {
    'DAT',
}

ENDIAN_STRINGS = {
    'L',  # Little-endian data
    'M',  # Big-endian data
}

EXTERNAL_PARAMETERS = {
    'Energy',
    'Temperature',
    'Time'
}

BITS_PER_BYTE = 8
