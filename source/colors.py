"""PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: March, 2017

Contained here are color definitions for use in color coding plots to
user selected areas in LEEM and LEED images.

Colors are chosen from Flat UI colors based on the Google Material Design UI
"""

from PyQt5 import QtGui


class Palette(object):
    """Store color info for plotting in RGB and QColor modes."""

    def __init__(self):
        """Setup RGB list as int8 and QColor in RGB int8 format."""
        self.color_palette = [(192, 57, 43),
                              (52, 152, 219),
                              (142, 68, 173),
                              (230, 126, 34),
                              (124, 75, 225),
                              (46, 204, 113),
                              (149, 165, 166),
                              (241, 196, 15),
                              (26, 188, 156),
                              (244, 114, 208)]
        self.qcolors = [QtGui.QColor(tup[0], tup[1], tup[2]) for tup in self.color_palette]
