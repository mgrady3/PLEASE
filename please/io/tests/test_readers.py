""" Unittests for image I/O """

import os
import pkg_resources
from unittest import TestCase

import numpy as np

from please.io.readers import read_image_data, read_raw_data


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
            read_raw_data(
                self.raw_data_file,
                height=height,
                width=width,
                bits_per_pixel=bits_per_pixel,
                byteorder=byteorder
            )

        # Then
        self.assertIn(expected_error, str(ctx.exception))
