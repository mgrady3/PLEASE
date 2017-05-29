"""PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: May, 2017

This file provides an interface for reading the raw file output from
Elmitec LEEM systems. The header of each file contains a lot of extraneous
information given that we are only interested in displaying the image.

The relevant bits required to display the image are Height, Width, BitsPerPixel.

UKSoft2001 UView Dat File Header Format:
  Fileheader  (104 bytes)
  Imageheader (48 bytes)
  Data (width x height x 2 bytes)

 struct UKFileHeader{    size of(UKFileHeader):104
    20 char id[20];
    2 short size;
    2 short version;
    2 short BitsPerPixel; (= 16 for Sensicam,  storage, not 12-bit acquisition)
    6  [not advertised 6-byte 'bye' for getting long to proper spot ]
        // 6 bytes inserted to get to next 8 byte boundary.
           LONGLONG seems to need to start at 8 byte boundary
    8 LONGLONG starttime;
    2 short ImageWidth;
    2 short ImageHeight;
    2 short NrImages;
    2 short spareShort;
    56 BYTE spare[56];
};

 struct UKImageHeader{    size of(UKImageHeader):48
  2	short size;
  2	short version;
  4    // 4 bytes inserted to get to next 8 byte boundary
  8	LONGLONG imagetime;
  4	long LEEMdata1_source;
  4	float LEEMdata1_data;
  2	short spin;
  2	short spareShort;
  4	float LEEMdata2_data;
 16	BYTE spare[16];
};

Note: The length of the header need not be exactly known.
It likely varies for different versions of UView. The above outline may change for future versions.

The required information is all located within the beginning
header section, beginning the header with index=0
    BitsPerPixel = bytes 24-25
    Width = bytes 40-41
    Height = bytes 42-43

Given this information, the total header size can be calculated dynamically for each file.

    Total File size = len(file.read())
    Required Image size = (BitsPerPixel//8)*Width*Height
    Header size = Total File size - Required Image size
    Image Data = f.read()[Header size:]
"""

import glob
import os
import struct


class UViewParser(object):
    """
    """
    def __init__(self, path):
        """
        """
        self.path = path

    def getFiles(self):
        """
        """
        self.files = glob.glob(os.path.join(self.path, "*.dat"))

    def parseFiles(self):
        """
        """
        if not self.files:
            print("Error: No .dat files found in {}".format(self.path))
            return None
        self.headerInfo = []
        for fl in self.files:
            with open(fl, 'rb') as f:
                # grab the first 100 bytes from each file
                # all required file info should be here
                header = f.read()[0:100]

            try:
                bits_per_pixel = struct.unpack('h', header[24:26])
            except struct.error:
                print("Error: Unable to read bits_per_pixel from header at bytes 24, 25 in file {}".format(fl))
                self.headerInfo = []
                return None
            try:
                width = struct.unpack('h', header[40:42])
            except struct.error:
                print("Error: Unable to read image width from header at bytes 40, 41 in file {}".format(fl))
                self.headerInfo = []
                return None
            try:
                height = struct.unpack('h', header[42:44])
            except struct.error:
                print("Error: Unable to read image height from header at bytes 42, 43 in file {}".format(fl))
                self.headerInfo = []
                return None
            self.headerInfo.append((bits_per_pixel, width, height))
        return self.headerInfo
