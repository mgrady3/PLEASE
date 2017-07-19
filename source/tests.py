"""
PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: July, 2017

Collection of tests for methods used in PLEASE

NOTE: This test suite is WOEFULLY incomplete. I am admitedly a novie when
it comes to writing unittests in scientific software. I hope to fill out
this suite with more relevant tests over time while I learn more about
the unit test ecosystem in python.

"""
import glob
import os
import unittest
import numpy as np
import LEEMFUNCTIONS as LF

from PIL import Image


class TestReadImage(unittest.TestCase):
    """Test LF.read_img().

    Override setUp and tearDown to generate/delete test data
    """

    dtypes = [np.uint8, np.uint16, np.uint32, np.uint64]
    dtype_strings = ['uint8', 'uint16', 'uint32', 'uint64']
    imtypes = ['.tif', '.png', '.jpg']

    # Flags for which tests are complete and ready to be used
    tests_complete = {
                        "test_read_images": False,
                        "test_8bit_images": True,
                        "test_16bitTiff": True
                     }

    def setUp(self):
        """Create test data."""
        self.source_path = os.path.dirname(LF.__file__)
        self.test_data_path = os.path.join(self.source_path, "unittest_data_tmp")
        if not os.path.exists(self.test_data_path):
            os.mkdir(self.test_data_path)
        return
        ###########################################################################
        # combinations = [(dat, im) for dat in self.dtypes for im in self.imtypes]

        # for dtype, imtype in combinations:
        #     self.createImage(dtype, imtype)
        ##########################################################################

    def tearDown(self):
        """Remove all temp files from self.test_data_path."""
        files = glob.glob(os.path.join(self.test_data_path, "*.*"))
        for fl in files:
            os.remove(fl)

    def createImage(self, dtype, imtype):
        """Create numpy array with given dtype then convert to PIL image.

        :param dtype: one of numpy data types listed in class variable dtpyes
        :param imtype: one of string file extenstion listed in class varaible imtypes
        """
        height, width = (1024, 1024)
        test_array = np.random.randint(0, 200, size=(height, width), dtype=dtype)
        idx = self.dtypes.index(dtype)
        im_name = "test_img_{0}_{1}".format(self.dtype_strings[idx], imtype)
        # You can't save certain dtypes as certain imtypes
        # if PIL throws an exception indicating this, just pass
        # this will save all possible combinations and pass on
        # combinations that Failed
        try:
            Image.fromarray(test_array).save(os.path.join(self.test_data_path, im_name))
        except (KeyError, OSError, TypeError):
            print("Failed to create Image with following paramters {}, {}".format(dtype, imtype))
            if os.path.exists(os.path.join(self.test_data_path, im_name)):
                os.remove(os.path.join(self.test_data_path, im_name))
            return
        print("Created Image with following paramters {}, {}".format(dtype, imtype))

    @unittest.skipUnless(tests_complete["test_8bit_images"], "Skipping incomplete test")
    def test_8bit_images(self):
        """Test LF.read_img with 8bit images."""
        dtype = self.dtypes[0]
        for imtype in self.imtypes:
            self.createImage(dtype, imtype)

        files = glob.glob(os.path.join(self.test_data_path, "*.*"))
        for fl in files:
            im = LF.read_img(os.path.join(self.test_data_path, fl))
            self.assertTrue(im.dtype == dtype)

    @unittest.skipUnless(tests_complete["test_16bitTiff"], "Skipping incomplete test.")
    @unittest.expectedFailure
    def test_16bitTiff(self):
        """Test LF.read_img() with 16bit TIFF."""
        dtype = self.dtypes[1]
        self.createImage(dtype, self.imtypes[0])
        files = glob.glob(os.path.join(self.test_data_path, "*.tif"))
        for fl in files:
            im = LF.read_img(os.path.join(self.test_data_path, fl))
            # NOTE: This should fail since read_img() uses .convert('L') which downscales to 8-bit
            self.assertTrue(im.dtype == dtype)

    @unittest.skipUnless(tests_complete["test_read_images"], "Skipping incomplete test.")
    def test_read_images(self):
        """Use LF.read_img to read the images created by createImage()."""
        files = glob.glob(os.path.join(self.test_data_path, "*.*"))
        for fl in files:
            im = LF.read_img(os.path.join(self.test_data_path, fl))

            tmp = fl.split("_")
            dtype_from_image_name = None
            for typ in self.dtype_strings:
                if typ in tmp:
                    dtype_from_image_name = typ
            if not dtype_from_image_name:
                print("Error reading image dtype from file name")
                break
            idx = self.dtype_strings.index(dtype_from_image_name)
            dtype = self.dtypes[idx]
            print("Testing dtype from image {}".format(fl))
            print("\t" + str(im.dtype))
            print("\t" + str(dtype_from_image_name))
            self.assertTrue(im.dtype == dtype)


if __name__ == '__main__':
    unittest.main()
