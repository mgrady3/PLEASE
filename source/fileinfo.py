"""PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: May, 2017

fileinfo.py

This file provides an input widget for the user to enter file information.
This is used to parse a directory of .dat files and strip their headers.
The result is a set of daw .dat files with only image data.
"""

from PyQt5 import QtCore, QtWidgets


class FileInfoWidget(QtWidgets.QWidget):
    """Widget to get User input for data file settings.

    Validates and emits settings as a dict to the main UI.
    """

    settings = QtCore.pyqtSignal(object)  # will emit a python dict object
    # finished = QtCore.pyqtSignal()

    def __init__(self):
        """."""
        self.layout = QtWidgets.QHBoxLayout()
        self.height_label = QtWidgets.QLabel("Enter Image Height: [int > 0]")
        self.width_label = QtWidgets.QLabel("Enter Image Width: [int > 0]")
        self.bit_size_label = QtWidgets.QLabel("Select bits per pixel: 8bit or 16bit")

        self.height_field = QtWidgets.QLineEdit()
        self.width_field = QtWidgets.QLineEdit()
        self.bit_size_menu = QtWidgets.QComboBox()
        self.bit_size_menu.addItem("8-bit")
        self.bit_size_menu.addItem("16-bit")

        self.submit_button = QtWidgets.QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.emitSettings)

        self.layout.addWidget(self.height_label)
        self.layout.addWidget(self.height_field)
        self.layout.addStretch()

        self.layout.addWidget(self.width_label)
        self.layout.addWidget(self.width_field)
        self.layout.addStretch()

        self.layout.addWidget(self.bit_size_label)
        self.layout.addWidget(self.bit_size_menu)
        self.layout.addStretch()

        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)
        self.show()

    def validateSettings(self):
        """Ensure User input is valid."""
        height = self.height_field.text()
        try:
            height = int(height)
        except ValueError:
            print("Error: Image height must be input as an integer.")
            return None
        if height <= 0:
            print("Error: Image height must be greater than zero.")
            return None

        width = self.width_field.text()
        try:
            width = int(width)
        except ValueError:
            print("Error: Image width must be input as an integer.")
            return None
        if width <= 0:
            print("Error: Image width must be greater than zero.")
            return None

        bit_size = self.bit_size_menu.currentText()
        if str(bit_size) == '16-bit':
            bit_size = 16
        elif str(bit_size) == '8-bit':
            bit_size = 8
        else:
            print("Error: Unknown bit size. Valid choices are 16-bit and 8-bit")
            return None

        return {'height': height,
                'width': width,
                'bit size': bit_size}

    def emitSettings(self):
        """Send dict of User settings to main UI thread."""
        self.user_settings = self.validateSettings()
        if self.user_settings is not None:
            self.settings.emit(self.user_settings)
            self.close()
        else:
            print("Error in User Settings. Please enter valid input.")
            return
