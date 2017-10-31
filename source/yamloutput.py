"""PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: October, 2017

This file contains a widget which provides a user interface to create an Experiment Configuration File,
which will be saved and output as a .yaml file. This file can then be loaded by PLEASE to facilitate the
loading of LEEM or LEED data sets.
"""
from PyQt5 import QtCore, QtWidgets


class ExperimentYAMLOutput(QtWidgets.QWidget):
    """UI Widget to generate Experiment Configuration Files in YAML format."""

    userData = QtCore.pyqtSignal(object)

    def __init__(self):
        """."""
        super(ExperimentYAMLOutput, self).__init__()
        self.setupLayout()
        self.dataPath = None
        self.pathButton.clicked.connect(self.getPath)
        self.doneButton.clicked.connect(self.parseInput)
        self.setWindowTitle("Enter Data Settings")
        self.show()

    def getPath(self):
        """Get Path to Data files from User."""
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Data Directory")
        if isinstance(path, tuple) and len(path) != 0:
            path = str(path[0])
        if path != "":
            self.dataPath = path
            self.pathText.setReadOnly(False)
            self.pathText.setText(path)
            self.pathText.setReadOnly(True)

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
        self.dataTypeMenu.addItem("Raw")
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

        # Time Series
        timeSeriesHBox = QtWidgets.QHBoxLayout()
        timeSeriesLabel = QtWidgets.QLabel("Interpret data as time series?")
        self.timeSeriesCheckBox = QtWidgets.QCheckBox("Enabled")
        self.timeSeriesCheckBox.stateChanged.connect(self.enableDisableTimeStepInput)
        timeSeriesHBox.addWidget(timeSeriesLabel)
        timeSeriesHBox.addStretch()
        timeSeriesHBox.addWidget(self.timeSeriesCheckBox)
        mainVBox.addLayout(timeSeriesHBox)

        # Time Step
        timeStepHBox = QtWidgets.QHBoxLayout()
        timeStepLabel = QtWidgets.QLabel("Time step between images in seconds [float]:")
        self.timeStepText = QtWidgets.QLineEdit()
        timeStepHBox.addWidget(timeStepLabel)
        timeStepHBox.addStretch()
        timeStepHBox.addWidget(self.timeStepText)
        mainVBox.addLayout(timeStepHBox)


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

    @QtCore.pyqtSlot(int)
    def enableDisableTimeStepInput(self, state):
        """Toggle ability to input a value in the Time Step QLineEdit based on QCheckBox state."""
        if state == 0:
            self.timeStepText.setEnabled(False)
        else:
            self.timeStepText.setEnabled(True)

    def parseInput(self):
        """Triggered when User clicks Done button.

        Ensure proper values are entered and that all fields are covered.
        """
        name = str(self.nameText.text())
        if name == '':
            print("Warning: No file name entered; defaulting to Experiment.yaml")
            name = 'Experiment.yaml'
        else:
            name += ".yaml"

        exptype = str(self.expTypeMenu.currentText()).upper()

        datatype = str(self.dataTypeMenu.currentText())

        fileext = str(self.fileTypeMenu.currentText()).lower()

        timeseries = self.timeSeriesCheckBox.isChecked()
        timestep = 0.0  # default value
        if timeseries:
            try:
                timestep = float(self.timeStepText.text())
            except ValueError:
                print("Error: Time Step must be a decimal number > 0 (ex: 0.1).")
                return
            if timestep < 0:
                print("Error: Time Step must be a decimal number > 0 (ex: 0.1).")
                return

        try:
            imht = int(self.htText.text())
        except ValueError:
            print("Error: Image Height must be an integer > 0 (ex: 1024).")
            return
        if imht <= 0:
            print("Error: Image Height must be an integer > 0 (ex: 1024).")
            return
        try:
            imwd = int(self.wdText.text())
        except ValueError:
            print("Error: Image Width must be an integer > 0 (ex: 1024).")
            return
        if imwd <= 0:
            print("Error: Image Height must be an integer > 0 (ex: 1024).")
            return

        try:
            minE = float(self.minEText.text())
        except ValueError:
            print("Error: Minimum energy must be a decimal number (ex: 0.1).")
            return
        try:
            maxE = float(self.maxEText.text())
        except ValueError:
            print("Error: Maximum energy must be a decimal number (ex: 0.1).")
            return
        if maxE <= minE:
            print("Error: Maximum Energy must be > Minimum Energy.")
            return
        try:
            stepE = float(self.stepEText.text())
        except ValueError:
            print("Error: Energy Step Size must be a decimal number (ex: 0.1).")
            return

        bitsize = str(self.bitSizeMenu.currentText())
        if bitsize == "16-bit":
            bitsize = 16
        else:
            bitsize = 8

        byteorder = str(self.byteOrderMenu.currentText())
        if byteorder == "LittleEndian":
            byteorder = "L"
        else:
            byteorder = "B"

        if self.dataPath is None:
            print("Error: You must select valid data path.")
            return

        settings = {
            'File Name': name,
            "Experiment Type": exptype,
            "Data Type": datatype,
            "File Format": fileext,
            "Time Series": timeseries,
            "Image Height": imht,
            "Image Width": imwd,
            "Minimum Energy": minE,
            "Maximum Energy": maxE,
            "Energy Step Size": stepE,
            "Data Path": self.dataPath,
            "Bit Depth": bitsize,
            "Byte Order": byteorder,
            "Time Step": timestep
        }
        self.userData.emit(settings)
        self.close()
