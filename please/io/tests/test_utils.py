""" Unit tests for File I/O helper functions """

import os
import pkg_resources
from unittest import TestCase

from please.io.utils import get_file_extension, is_image_file, is_raw_file


class TestIOUtils(TestCase):

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
        cls.no_extension = '/home/user/some_other_file'

    def test_get_file_extension(self):
        # Given
        expected = '.dat'

        # When
        ext = get_file_extension(self.raw_data_file)

        # Then
        self.assertEqual(ext, expected)

        # Given
        expected = '.png'

        # When
        ext = get_file_extension(self.img_file)

        # Then
        self.assertEqual(ext, expected)

        # Given
        expected = ''

        # When
        ext = get_file_extension(self.no_extension)

        # Then
        self.assertEqual(ext, expected)

    def test_is_image_file(self):
        # Then
        self.assertTrue(is_image_file(self.img_file))
        self.assertFalse(is_image_file(self.raw_data_file))
        self.assertFalse(is_image_file(self.no_extension))

    def test_is_raw_file(self):
        # Then
        self.assertTrue(is_raw_file(self.raw_data_file))
        self.assertFalse(is_raw_file(self.img_file))
        self.assertFalse(is_raw_file(self.no_extension))
