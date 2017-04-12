"""PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: April, 2017

This file contains a widget which provides a user interface to create an Experiment Configuration File,
which will be saved and output as a .yaml file. This file can then be loaded by PLEASE to facilitate the
loading of LEEM or LEED data sets.
"""
from PyQt5 import QtWidgets


class ExperimentYAMLOutput(QtWidgets.QWidget):
    """UI Widget to generate Experiment Configuration Files in YAML format."""

    def __init__(self):
        """."""
        super(ExperimentYAMLOutput, self).__init__()
        self.setupLayout()
        self.show()

    def setupLayout(self):
        """Setup Widget UI Layout."""
        mainVBox = QtWidgets.QVBoxLayout()

        # File Name
        nameHBox = QtWidgets.QHBoxLayout()
        nameLabel = QtWidgets.QLabel("Enter File Name (no extension):")
        self.nameText = QtWidgets.QLineEdit()
        nameHBox.addWidget(nameLabel)
        nameHBox.addStretch()
        nameHBox.addWidget(self.nameText)
        mainVBox.addLayout(nameHBox)

        # Experiment Type
        expTypeHBox = QtWidgets.QHBoxLayout()
        expTypeLabel = QtWidgets.QLabel("Choose Experiment Type:")
        self.expTypeMenu = QtWidgets.QComboBox()
        self.expTypeMenu.addItem("LEEM")
        self.expTypeMenu.addItem("LEED")
        expTypeHBox.addWidget(expTypeLabel)
        expTypeHBox.addStretch()
        expTypeHBox.addWidget(self.expTypeMenu)
        mainVBox.addLayout(expTypeHBox)

        # Data Type
        dataTypeHBox = QtWidgets.QHBoxLayout()
        dataTypeLabel = QtWidgets.QLabel("Choose Data Type:")
        self.dataTypeMenu = QtWidgets.QComboBox()
        self.dataTypeMenu.addItem("RAW")
        self.dataTypeMenu.addItem("Image")
        dataTypeHBox.addWidget(dataTypeLabel)
        dataTypeHBox.addStretch()
        dataTypeHBox.addWidget(self.dataTypeMenu)
        mainVBox.addLayout(dataTypeHBox)

        # File Type
        fileTypeHBox = QtWidgets.QHBoxLayout()
        fileTypeLabel = QtWidgets.QLabel("Choose File Type:")
        self.fileTypeMenu = QtWidgets.QComboBox()
        self.fileTypeMenu.addItem(".dat")
        self.fileTypeMenu.addItem(".png")
        self.fileTypeMenu.addItem(".tif")
        fileTypeHBox.addWidget(fileTypeLabel)
        fileTypeHBox.addStretch()
        fileTypeHBox.addWidget(self.fileTypeMenu)
        mainVBox.addLayout(fileTypeHBox)

        # Image Parameters
        mainVBox.addWidget(QtWidgets.QLabel("Image Parameters:"))
        htHBox = QtWidgets.QHBoxLayout()
        htHBox.addStretch()
        htHBox.addWidget(QtWidgets.QLabel("Enter Height [Integer > 0]:"))
        self.htText = QtWidgets.QLineEdit()
        htHBox.addStretch()
        htHBox.addWidget(self.htText)
        mainVBox.addLayout(htHBox)

        wdHBox = QtWidgets.QHBoxLayout()
        wdHBox.addStretch()
        wdHBox.addWidget(QtWidgets.QLabel("Enter Width [Integer > 0]:"))
        self.wdText = QtWidgets.QLineEdit()
        wdHBox.addStretch()
        wdHBox.addWidget(self.wdText)
        mainVBox.addLayout(wdHBox)

        # Energy Parameters
        mainVBox.addWidget(QtWidgets.QLabel("Energy Parameters:"))
        minEHBox = QtWidgets.QHBoxLayout()
        minEHBox.addStretch()
        minEHBox.addWidget(QtWidgets.QLabel("Enter Minimum Energy [float]:"))
        minEHBox.addStretch()
        self.minEText = QtWidgets.QLineEdit()
        minEHBox.addWidget(self.minEText)
        mainVBox.addLayout(minEHBox)

        maxEHBox = QtWidgets.QHBoxLayout()
        maxEHBox.addStretch()
        maxEHBox.addWidget(QtWidgets.QLabel("Enter Maximum Energy [float]:"))
        maxEHBox.addStretch()
        self.maxEText = QtWidgets.QLineEdit()
        maxEHBox.addWidget(self.maxEText)
        mainVBox.addLayout(maxEHBox)

        stepEHBox = QtWidgets.QHBoxLayout()
        stepEHBox.addStretch()
        stepEHBox.addWidget(QtWidgets.QLabel("Enter Energy Step size [float]:"))
        stepEHBox.addStretch()
        self.stepEText = QtWidgets.QLineEdit()
        stepEHBox.addWidget(self.stepEText)
        mainVBox.addLayout(stepEHBox)

        # Data Parameters:
        pathHBox = QtWidgets.QHBoxLayout()
        pathHBox.addStretch()
        pathLabel = QtWidgets.QLabel("Click to select data path:")
        pathHBox.addWidget(pathLabel)
        self.pathButton = QtWidgets.QPushButton("Select Path", self)
        pathHBox.addWidget(self.pathButton)
        self.pathText = QtWidgets.QLineEdit()
        self.pathText.setReadOnly(True)
        pathHBox.addWidget(self.pathText)
        mainVBox.addLayout(pathHBox)

        bitSizeHBox = QtWidgets.QHBoxLayout()
        bitSizeHBox.addStretch()
        bitSizeHBox.addWidget(QtWidgets.QLabel("Choose Bit Depth (8bit or 16bit)"))
        self.bitSizeMenu = QtWidgets.QComboBox()
        self.bitSizeMenu.addItem("8-bit")
        self.bitSizeMenu.addItem("16-bit")
        bitSizeHBox.addWidget(self.bitSizeMenu)
        mainVBox.addLayout(bitSizeHBox)

        byteOrderHBox = QtWidgets.QHBoxLayout()
        byteOrderHBox.addStretch()
        byteOrderHBox.addWidget(QtWidgets.QLabel("Choose Byte Order (LittleEndian or BigEndian)"))
        self.byteOrderMenu = QtWidgets.QComboBox()
        self.byteOrderMenu.addItem("LittleEndian")
        self.byteOrderMenu.addItem("BigEndian")
        byteOrderHBox.addWidget(self.byteOrderMenu)
        mainVBox.addLayout(byteOrderHBox)

        mainVBox.addStretch()
        doneButtonHBox = QtWidgets.QHBoxLayout()
        doneButtonHBox.addStretch()
        self.doneButton = QtWidgets.QPushButton("Done", self)
        doneButtonHBox.addWidget(self.doneButton)
        mainVBox.addLayout(doneButtonHBox)
        self.setLayout(mainVBox)
