""" Unit tests for image models """

from unittest import TestCase

import numpy as np

from please.model.image import LEEDImage, LEEMImage

class TestIEMImage(TestCase):

    def setUp(self):
        self.height = 600
        self.width = 592
        self.fake_data = np.zeros((self.height, self.width))
        self.leem = LEEMImage(data=self.fake_data)
        self.leed = LEEDImage(data=self.fake_data)
        self.images = [self.leed, self.leem]

    def test__get_width(self):
        for img in self.images:
            self.assertEqual(img.width, self.width)

    def test__get_height(self):
        for img in self.images:
            self.assertEqual(img.height, self.height)

    def test__get_shape(self):
        for img in self.images:
            self.assertEqual(img.shape, (self.height, self.width))

    def test_image_type(self):
        self.assertEqual(self.leem.image_type, 'LEEM')
        self.assertEqual(self.leed.image_type, 'LEED')