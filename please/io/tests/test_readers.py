""" Unittests for image I/O """

import os
import pkg_resources
from unittest import TestCase

import numpy as np

from please.io.readers import read_image_data, read_raw_data, _get_dtype_string


class TestImageFileIO(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.raw_data_file = pkg_resources.resource_filename(
            'please.io.tests',
            os.path.join('data', '20141023_01_100.dat')
        )
        cls.img_file = pkg_resources.resource_filename(
            'please.io.tests',
            os.path.join('data', '20141023_01_100.png')
        )


    def test__get_dtype_string(self):
        # Given
        bits = 8
        byteorder = 'L'
        expected = '<u1'

        # When
        format_string = _get_dtype_string(bits, byteorder)

        # Then
        self.assertEqual(format_string, expected)

        # Given
        bits = 8
        byteorder = 'B'
        expected = '>u1'

        # When
        format_string = _get_dtype_string(bits, byteorder)

        # Then
        self.assertEqual(format_string, expected)

        # Given
        bits = 16
        byteorder = 'L'
        expected = '<u2'

        # When
        format_string = _get_dtype_string(bits, byteorder)

        # Then
        self.assertEqual(format_string, expected)

        # Given
        bits = 16
        byteorder = 'B'
        expected = '>u2'

        # When
        format_string = _get_dtype_string(bits, byteorder)

        # Then
        self.assertEqual(format_string, expected)

    def test__get_dtype_string_raises_value_error(self):
        # Given
        bits = 32
        byteorder = 'L'

        # When
        with self.assertRaisesRegex(ValueError, 'Unsupported bit size'):
            _get_dtype_string(bits, byteorder)

        # Given
        bits = 16
        byteorder = 'ABC123'

        # When
        with self.assertRaisesRegex(ValueError, 'Unsupported byteorder'):
            _get_dtype_string(bits, byteorder)

    def test_read_image_data(self):
        # Given
        expected_shape = (600, 592)

        # When
        data = read_image_data(self.img_file)

        # Then
        self.assertIsInstance(data, np.ndarray)
        self.assertEqual(data.shape, expected_shape)

    def test_read_raw_data(self):
        # Given
        bits_per_pixel = 16
        byteorder = 'L'
        height = 600
        width = 592
        expected_shape = (height, width)

        # When
        data = read_raw_data(
            self.raw_data_file,
            height=height,
            width=width,
            bits_per_pixel=bits_per_pixel,
            byteorder=byteorder
        )

        # Then
        self.assertIsInstance(data, np.ndarray)
        self.assertEqual(data.shape, expected_shape)

    def test_read_raw_data_raises_for_bad_params(self):
        # Given
        bits_per_pixel = 16
        byteorder = 'L'
        height = 6000  # Wrong height
        width = 5920  # Wrong width
        expected_error = " Image parameters do not match the data file."
        # When
        with self.assertRaises(ValueError) as ctx:
            data = read_raw_data(
                self.raw_data_file,
                height=height,
                width=width,
                bits_per_pixel=bits_per_pixel,
                byteorder=byteorder
            )

        # Then
        self.assertIn(expected_error, str(ctx.exception))
