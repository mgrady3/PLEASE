""" This module contains an implementation of the base IEMImage class, used
to represent Electron Microscopy image data for common formats such as
LEEM/LEED data.
"""

from .interfaces import IEMImage


class LEEMImage(IEMImage):

    def __init__(self, **traits):
        super().__init__(**traits)
        self.image_type = 'LEEM'


class LEEDImage(IEMImage):

    def __init__(self, **traits):
        super().__init__(**traits)
        self.image_type = 'LEED'