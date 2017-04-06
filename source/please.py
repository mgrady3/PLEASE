"""PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: April, 2017

PLEASE provides a convienient Graphical User Interface for exploration and
analysis of Low Energy Electron Microscopy and Diffraction data sets.
Specifically, emphasis is placed on visualization of Intensity-Voltage data
sets and providing an easy popint and click method for extracting I(V) curves.

Analysis of LEEM-I(V) and LEED-I(V) data sets provides inisght with atomic
scale resolution to the surface structure of a wide array of materials from
semiconductors to metals in bulk or thin film as well as single layer 2D materials.
"""

# Stdlib and Scientific Stack imports
import os
import sys
import yaml
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets

# local project imports
import LEEMFUNCTIONS as LF
from configinfo import output_environment_config
from colors import Palette
from data import LeedData, LeemData
from experiment import Experiment
from qthreads import WorkerThread
from terminal import MessageConsole

__Version = '1.0.0'


class ExtendedCrossHair(QtCore.QObject):
    """Set of perpindicular InfiniteLines tracking mouse postion."""

    def __init__(self):
        """."""
        super(ExtendedCrossHair, self).__init__()
        self.hline = pg.InfiniteLine(angle=0, movable=False)
        self.vline = pg.InfiniteLine(angle=90, movable=False)
        self.curPos = (0, 0)  # store (x, y) mouse position


class MainWindow(QtWidgets.QMainWindow):
    """Top level conatiner to wrap Viewer object.

    Provides dockable interface.
    Provides Menubar - to be implemented later
    """

    def __init__(self, v=None):
        """Parameter v tracks the current PLEASE version number."""
        super(QtWidgets.QMainWindow, self).__init__()
        if v is not None:
            self.setWindowTitle("PLEASE v. {}".format(v))
        else:
            self.setWindowTitle("PLEASE")
        self.viewer = Viewer(parent=self)
        self.setCentralWidget(self.viewer)

        self.menubar = self.menuBar()
        self.setupMenu()

        self.setupDockableWidgets()
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockwidget)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.bottomdock)

    def setupDockableWidgets(self):
        """Dock control and information widgets to main window."""
        # Leftside button widgets
        self.dockwidget = QtWidgets.QDockWidget(self)

        # setup pushbutton functions
        self.groupbox = QtWidgets.QGroupBox()
        self.buttonboxlayout = QtWidgets.QVBoxLayout()
        self.loadexperimentbutton = QtWidgets.QPushButton("Load Experiment")
        self.loadexperimentbutton.clicked.connect(self.viewer.load_experiment)
        self.outputLEEMbutton = QtWidgets.QPushButton("Output LEEM Data")
        self.outputLEEDbutton = QtWidgets.QPushButton("Output LEED Data")
        self.outputLEEMbutton.clicked.connect(lambda: self.viewer.outputIV(datatype='LEEM'))
        self.outputLEEDbutton.clicked.connect(lambda: self.viewer.outputIV(datatype='LEED'))
        self.quitbutton = QtWidgets.QPushButton("Quit")
        self.quitbutton.clicked.connect(self.quit)
        self.buttonboxlayout.addWidget(self.loadexperimentbutton)
        self.buttonboxlayout.addWidget(self.outputLEEMbutton)
        self.buttonboxlayout.addWidget(self.outputLEEDbutton)
        self.buttonboxlayout.addStretch()
        self.buttonboxlayout.addWidget(self.quitbutton)
        self.groupbox.setLayout(self.buttonboxlayout)

        self.dockwidget.setWidget(self.groupbox)

        # bottom message console
        self.bottomdock = QtWidgets.QDockWidget(self)
        self.console = MessageConsole()
        self.bottomdock.setWidget(self.console)

    def setupMenu(self):
        """Set Menu actions for LEEM and LEED."""
        fileMenu = self.menubar.addMenu("File")
        LEEMMenu = self.menubar.addMenu("LEEM")
        LEEDMenu = self.menubar.addMenu("LEED")
        helpMenu = self.menubar.addMenu("Help")

        # File menu
        self.exitAction = QtWidgets.QAction("Exit", self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(self.quit)
        fileMenu.addAction(self.exitAction)

        # LEEM menu
        self.outputLEEMAction = QtWidgets.QAction("Output I(V)", self)
        self.outputLEEMAction.triggered.connect(lambda: self.viewer.outputIV(datatype='LEEM'))
        LEEMMenu.addAction(self.outputLEEMAction)

        self.clearLEEMAction = QtWidgets.QAction("Clear I(V)", self)
        self.clearLEEMAction.triggered.connect(self.viewer.clearLEEMIV)
        LEEMMenu.addAction(self.clearLEEMAction)

        self.enableLEEMRectAction = QtWidgets.QAction("Enable LEEM Window Extraction", self)
        self.enableLEEMRectAction.triggered.connect(self.viewer.enableLEEMWindow)
        LEEMMenu.addAction(self.enableLEEMRectAction)

        self.disableLEEMRectAction = QtWidgets.QAction("Disable LEEM Window Extraction", self)
        self.disableLEEMRectAction.triggered.connect(self.viewer.disableLEEMWindow)
        LEEMMenu.addAction(self.disableLEEMRectAction)

        self.clearWindowsAction = QtWidgets.QAction("Clear Windows", self)
        self.clearWindowsAction.triggered.connect(self.viewer.clearLEEMWindows)
        LEEMMenu.addAction(self.clearWindowsAction)

        self.extractLEEMWindowAction = QtWidgets.QAction("Extract I(V) from Windows", self)
        self.extractLEEMWindowAction.triggered.connect(self.viewer.extractLEEMWindows)
        self.extractLEEMWindowAction.setEnabled(self.viewer.LEEMRectWindowEnabled)
        LEEMMenu.addAction(self.extractLEEMWindowAction)

        self.toggleLEEMReflectivityAction = QtWidgets.QAction("Toggle Reflectivty", self)
        self.toggleLEEMReflectivityAction.triggered.connect(lambda: self.viewer.toggleReflectivity(data="LEEM"))
        LEEMMenu.addAction(self.toggleLEEMReflectivityAction)

        # LEED menu
        self.extractAction = QtWidgets.QAction("Extract I(V)", self)
        # extractAction.setShortcut("Ctrl-E")
        self.extractAction.triggered.connect(self.viewer.processLEEDIV)
        LEEDMenu.addAction(self.extractAction)

        self.clearAction = QtWidgets.QAction("Clear I(V)", self)
        self.clearAction.triggered.connect(self.viewer.clearLEEDIV)
        LEEDMenu.addAction(self.clearAction)

        self.toggleLEEDReflectivityAction = QtWidgets.QAction("Toggle Reflectivty", self)
        self.toggleLEEDReflectivityAction.triggered.connect(lambda: self.viewer.toggleReflectivity(data="LEED"))
        LEEDMenu.addAction(self.toggleLEEDReflectivityAction)

        # Help menu
        self.genConfigInfoFileAction = QtWidgets.QAction("Generate User Config File", self)
        self.genConfigInfoFileAction.triggered.connect(output_environment_config)
        helpMenu.addAction(self.genConfigInfoFileAction)

    @staticmethod
    def quit():
        """."""
        QtWidgets.QApplication.instance().quit()


class Viewer(QtWidgets.QWidget):
    """Main Container for Viewing LEEM and LEED data."""

    def __init__(self, parent=None):
        """Initialize main LEEM and LEED data stucts.

        Setup Tab structure
        Connect key/mouse event hooks to image plot widgets
        """
        super(QtWidgets.QWidget, self).__init__(parent=parent)
        self.initData()
        self.layout = QtWidgets.QVBoxLayout()

        self.tabs = QtWidgets.QTabWidget()
        self.LEEMTab = QtWidgets.QWidget()
        self.LEEDTab = QtWidgets.QWidget()
        self.ConfigTab = QtWidgets.QWidget()
        self.initLEEMTab()
        self.initLEEDTab()
        self.initConfigTab()
        self.tabs.addTab(self.LEEMTab, "LEEM-I(V)")
        self.initLEEMEventHooks()
        self.initLEEDEventHooks()
        self.tabs.addTab(self.LEEDTab, "LEED-I(V)")
        self.tabs.addTab(self.ConfigTab, "Config")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.show()

    def initData(self):
        """Specific initialization.

        Certain attributes require initialization so that their signals
        can be accessed.
        """
        self.staticLEEMplot = pg.PlotWidget()  # not displayed until User clicks LEEM image
        self.staticLEEMplot.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # container for circular patches indicating locations of User clicks in LEEM image
        self.LEEMcircs = []
        self.LEEMclicks = 0

        # container for QRectF patches to be drawn atop LEEDimage
        self.LEEDrects = []  # stored as tuple (rect, pen)
        self.LEEDclicks = 0
        self.LEEDclickpos = []  # container for position of LEED clicks in array coordinate system
        self.boxrad = 20  # Integration windows are rectangles 2*boxrad x 2*boxrad

        self.threads = []  # container for QThread objects used for outputting files

        self.colors = Palette().color_palette
        self.qcolors = Palette().qcolors
        self.leemdat = LeemData()
        self.leeddat = LeedData()
        self.LEEMselections = []  # store coords of leem clicks in (r,c) format
        self.LEEDclickpos = []  # store coords of leed clicks in (r,c) format
        self.LEEMRectWindowEnabled = False

        self.smoothLEEDplot = False
        self.smoothLEEMplot = False
        self.smoothLEEDoutput = False
        self.smoothLEEMoutput = False
        self.LEEDWindowType = 'flat'
        self.LEEMWindowType = 'flat'
        self.LEEDWindowLen = 4
        self.LEEMWindowLen = 4

        self.exp = None  # overwritten on load with Experiment object
        self.hasdisplayedLEEMdata = False
        self.hasdisplayedLEEDdata = False

        # flags for plotting reflectivty rathet than intensity
        self.rescaleLEEMIntensity = False
        self.rescaleLEEDIntensity = False
        self.curLEEMIndex = 0
        self.curLEEDIndex = 0
        dummydata = np.zeros((10, 10))
        self.LEEMimage = pg.ImageItem(dummydata)  # required for signal hook
        self.LEEDimage = pg.ImageItem(dummydata)
        # self.LEEDimage = pg.ImageItem(dummydata)  # required for signal hook
        self.labelStyle = {'color': '#FFFFFF',
                           'font-size': '16pt'}
        self.boxrad = 20

    def initLEEMTab(self):
        """Setup Layout of LEEM Tab."""
        self.LEEMTabLayout = QtWidgets.QHBoxLayout()
        imvbox = QtWidgets.QVBoxLayout()
        imtitlehbox = QtWidgets.QHBoxLayout()

        self.LEEMimtitle = QtWidgets.QLabel("LEEM Real Space Image")
        imtitlehbox.addStretch()
        imtitlehbox.addWidget(self.LEEMimtitle)
        imtitlehbox.addStretch()
        imvbox.addLayout(imtitlehbox)
        self.LEEMimageplotwidget = pg.PlotWidget()
        # disable mouse pan on left click
        self.LEEMimageplotwidget.getPlotItem().getViewBox().setMouseEnabled(x=False, y=False)

        self.LEEMimageplotwidget.hideAxis("bottom")
        self.LEEMimageplotwidget.hideAxis("left")
        # self.LEEMimageplotwidget.setTitle("LEEM Real Space Image",
        #                                  size='18pt', color='#FFFFFF')
        imvbox.addWidget(self.LEEMimageplotwidget)
        self.LEEMTabLayout.addLayout(imvbox)

        ivvbox = QtWidgets.QVBoxLayout()
        titlehbox = QtWidgets.QHBoxLayout()
        self.LEEMIVTitle = QtWidgets.QLabel("LEEM-I(V)")
        titlehbox.addStretch()
        titlehbox.addWidget(self.LEEMIVTitle)
        titlehbox.addStretch()
        ivvbox.addLayout(titlehbox)

        self.LEEMivplotwidget = pg.PlotWidget()
        self.LEEMivplotwidget.setLabel('bottom',
                                       'Energy', units='eV',
                                       **self.labelStyle)
        self.LEEMivplotwidget.setLabel('left',
                                       'Intensity', units='arb units',
                                       **self.labelStyle)
        yaxis = self.LEEMivplotwidget.getAxis("left")
        # y axis is 'arbitrary units'; we don't want kilo or mega arbitrary units etc...
        yaxis.enableAutoSIPrefix(False)

        self.LEEMimageplotwidget.addItem(self.LEEMimage)
        ivvbox.addWidget(self.LEEMivplotwidget)
        self.LEEMTabLayout.addLayout(ivvbox)
        self.LEEMTab.setLayout(self.LEEMTabLayout)

    def initConfigTab(self):
        """Setup Layout of Config Tab."""
        # configTabGroupbox = QtWidgets.QGroupBox()
        configtabBottomButtonHBox = QtWidgets.QHBoxLayout()
        # configTabGroupButtonBox = QtWidgets.QHBoxLayout()
        configTabVBox = QtWidgets.QVBoxLayout()

        # smooth settings
        smoothLEEDVBox = QtWidgets.QVBoxLayout()
        smoothColumn = QtWidgets.QHBoxLayout()
        # smoothGroupBox = QtWidgets.QGroupBox()

        # LEED
        self.LEEDSettingsLabel = QtWidgets.QLabel("LEED Data Smoothing Settings")
        smoothLEEDVBox.addWidget(self.LEEDSettingsLabel)

        self.smoothLEEDCheckBox = QtWidgets.QCheckBox()
        self.smoothLEEDCheckBox.setText("Enable Smoothing")
        self.smoothLEEDCheckBox.stateChanged.connect(lambda: self.smoothing_statechange(data='LEED'))
        smoothLEEDVBox.addWidget(self.smoothLEEDCheckBox)

        window_LEED_hbox = QtWidgets.QHBoxLayout()
        self.LEED_window_label = QtWidgets.QLabel("Select Window Type")
        self.smooth_LEED_window_type_menu = QtWidgets.QComboBox()
        self.smooth_LEED_window_type_menu.addItem("Flat")
        self.smooth_LEED_window_type_menu.addItem("Hanning")
        self.smooth_LEED_window_type_menu.addItem("Hamming")
        self.smooth_LEED_window_type_menu.addItem("Bartlett")
        self.smooth_LEED_window_type_menu.addItem("Blackman")
        window_LEED_hbox.addWidget(self.LEED_window_label)
        window_LEED_hbox.addWidget(self.smooth_LEED_window_type_menu)
        smoothLEEDVBox.addLayout(window_LEED_hbox)

        LEED_window_len_box = QtWidgets.QHBoxLayout()
        self.LEED_window_len_label = QtWidgets.QLabel("Enter Window Length [even integer]")
        self.LEED_window_len_entry = QtWidgets.QLineEdit()

        LEED_window_len_box.addWidget(self.LEED_window_len_label)
        LEED_window_len_box.addWidget(self.LEED_window_len_entry)
        smoothLEEDVBox.addLayout(LEED_window_len_box)

        self.apply_settings_LEED_button = QtWidgets.QPushButton("Apply Smoothing Settings", self)
        self.apply_settings_LEED_button.clicked.connect(lambda: self.validate_smoothing_settings(but='LEED'))
        smoothLEEDVBox.addWidget(self.apply_settings_LEED_button)

        smoothColumn.addLayout(smoothLEEDVBox)
        smoothColumn.addStretch()
        smoothColumn.addWidget(self.v_line())
        smoothColumn.addStretch()

        # LEEM
        smooth_LEEM_vbox = QtWidgets.QVBoxLayout()
        smooth_group = QtWidgets.QGroupBox()

        self.LEEM_settings_label = QtWidgets.QLabel("LEEM Data Smoothing Settings")
        smooth_LEEM_vbox.addWidget(self.LEEM_settings_label)

        self.smoothLEEMCheckBox = QtWidgets.QCheckBox()
        self.smoothLEEMCheckBox.setText("Enable Smoothing")
        self.smoothLEEMCheckBox.stateChanged.connect(lambda: self.smoothing_statechange(data='LEEM'))
        smooth_LEEM_vbox.addWidget(self.smoothLEEMCheckBox)

        window_LEEM_hbox = QtWidgets.QHBoxLayout()
        self.LEEM_window_label = QtWidgets.QLabel("Select Window Type")
        self.smooth_LEEM_window_type_menu = QtWidgets.QComboBox()
        self.smooth_LEEM_window_type_menu.addItem("Flat")
        self.smooth_LEEM_window_type_menu.addItem("Hanning")
        self.smooth_LEEM_window_type_menu.addItem("Hamming")
        self.smooth_LEEM_window_type_menu.addItem("Bartlett")
        self.smooth_LEEM_window_type_menu.addItem("Blackman")
        window_LEEM_hbox.addWidget(self.LEEM_window_label)
        window_LEEM_hbox.addWidget(self.smooth_LEEM_window_type_menu)
        smooth_LEEM_vbox.addLayout(window_LEEM_hbox)

        LEEM_window_len_box = QtWidgets.QHBoxLayout()
        self.LEEM_window_len_label = QtWidgets.QLabel("Enter Window Length [even integer]")
        self.LEEM_window_len_entry = QtWidgets.QLineEdit()

        LEEM_window_len_box.addWidget(self.LEEM_window_len_label)
        LEEM_window_len_box.addWidget(self.LEEM_window_len_entry)
        smooth_LEEM_vbox.addLayout(LEEM_window_len_box)

        self.apply_settings_LEEM_button = QtWidgets.QPushButton("Apply Smoothing Settings", self)
        self.apply_settings_LEEM_button.clicked.connect(lambda: self.validate_smoothing_settings(but="LEEM"))
        smooth_LEEM_vbox.addWidget(self.apply_settings_LEEM_button)

        smoothColumn.addLayout(smooth_LEEM_vbox)
        smooth_group.setLayout(smoothColumn)

        configTabVBox.addWidget(smooth_group)
        configTabVBox.addWidget(self.h_line())

        # LEED rect  size settings
        RectSettingGroupBox = QtWidgets.QGroupBox()
        LEEDRectSettingHBox = QtWidgets.QHBoxLayout()
        LEEDRectSettingVBox = QtWidgets.QVBoxLayout()
        RectSettingLabel = QtWidgets.QLabel("Enter LEED Window Side Length [even integer]")
        LEEDRectSettingVBox.addWidget(RectSettingLabel)
        self.LEEDRectEntry = QtWidgets.QLineEdit()
        entryHBox = QtWidgets.QHBoxLayout()
        entryHBox.addWidget(self.LEEDRectEntry)
        entryHBox.addStretch()
        self.LEEDRectApplyButton = QtWidgets.QPushButton("Apply Window Size", self)
        self.LEEDRectApplyButton.clicked.connect(self.apply_LEED_window_size)
        RectButtonHBox = QtWidgets.QHBoxLayout()
        RectButtonHBox.addWidget(self.LEEDRectApplyButton)
        RectButtonHBox.addStretch()

        LEEDRectSettingVBox.addLayout(entryHBox)
        LEEDRectSettingVBox.addLayout(RectButtonHBox)

        LEEDRectSettingHBox.addLayout(LEEDRectSettingVBox)
        LEEDRectSettingHBox.addStretch()

        RectSettingGroupBox.setLayout(LEEDRectSettingHBox)
        configTabVBox.addWidget(RectSettingGroupBox)

        configTabVBox.addStretch()

        configtabBottomButtonHBox.addStretch(1)
        # configtabBottomButtonHBox.addWidget(self.quitbut)
        configTabVBox.addLayout(configtabBottomButtonHBox)
        self.ConfigTab.setLayout(configTabVBox)

    def initLEEDTab(self):
        """Setup Layout of LEED Tab."""
        self.LEEDTabLayout = QtWidgets.QHBoxLayout()

        self.imvbox = QtWidgets.QVBoxLayout()
        self.ivvbox = QtWidgets.QVBoxLayout()

        imtitlehbox = QtWidgets.QHBoxLayout()
        self.LEEDTitle = QtWidgets.QLabel("Reciprocal Space LEED Image")
        imtitlehbox.addStretch()
        imtitlehbox.addWidget(self.LEEDTitle)
        imtitlehbox.addStretch()
        self.imvbox.addLayout(imtitlehbox)

        self.LEEDimagewidget = pg.PlotWidget()
        # disable mouse pan on left click
        self.LEEDimagewidget.getPlotItem().getViewBox().setMouseEnabled(x=False, y=False)
        self.LEEDimagewidget.hideAxis("bottom")
        self.LEEDimagewidget.hideAxis("left")
        self.LEEDimagewidget.addItem(self.LEEDimage)  # dummy data
        self.imvbox.addWidget(self.LEEDimagewidget)
        self.LEEDTabLayout.addLayout(self.imvbox)

        ivtitlehbox = QtWidgets.QHBoxLayout()
        ivtitlehbox.addStretch()
        self.LEEDIVTitle = QtWidgets.QLabel("LEED-I(V)")
        ivtitlehbox.addWidget(self.LEEDIVTitle)
        ivtitlehbox.addStretch()
        self.ivvbox.addLayout(ivtitlehbox)
        self.LEEDivplotwidget = pg.PlotWidget()
        self.LEEDivplotwidget.setLabel('bottom',
                                       'Energy', units='eV',
                                       **self.labelStyle)
        self.LEEDivplotwidget.setLabel('left',
                                       'Intensity', units='arb units',
                                       **self.labelStyle)
        yaxis = self.LEEDivplotwidget.getAxis("left")
        # y axis is 'arbitrary units'; we don't want kilo or mega arbitrary units etc...
        yaxis.enableAutoSIPrefix(False)

        self.ivvbox.addWidget(self.LEEDivplotwidget)
        self.LEEDTabLayout.addLayout(self.ivvbox)
        self.LEEDTab.setLayout(self.LEEDTabLayout)

    def initLEEMEventHooks(self):
        """Setup event hooks for mouse click and mouse move.

        Signals beginning with 'sig' are defined by pyqtgraph
        as opposed to being defined in Qt.
        """
        # LEEM #
        # signals
        self.sigmcLEEM = self.LEEMimage.scene().sigMouseClicked
        self.sigmmvLEEM = self.LEEMimage.scene().sigMouseMoved

        self.sigmcLEEM.connect(self.handleLEEMClick)
        self.sigmmvLEEM.connect(self.handleLEEMMouseMoved)

    def initLEEDEventHooks(self):
        """Setup event hooks for mouse click in LEEDimagewidget."""
        self.sigmcLEED = self.LEEDimage.scene().sigMouseClicked
        self.sigmcLEED.connect(self.handleLEEDClick)

    @staticmethod
    def h_line():
        """Convienience to quickly add UI separators."""
        f = QtWidgets.QFrame()
        f.setFrameShape(QtWidgets.QFrame.HLine)
        f.setFrameShadow(QtWidgets.QFrame.Sunken)
        return f

    @staticmethod
    def v_line():
        """Convienience to quickly add UI separators."""
        f = QtWidgets.QFrame()
        f.setFrameShape(QtWidgets.QFrame.VLine)
        f.setFrameShadow(QtWidgets.QFrame.Sunken)
        return f

    def load_experiment(self):
        """Query User for YAML config file to load experiment settings.

        Adapted from my other project https://www.github.com/mgrady3/pLEASE
        """
        yamlFilter = "YAML (*.yaml);;YML (*.yml);;All Files (*)"
        homeDir = os.getenv("HOME")
        caption = "Select YAML Experiment Config File"
        fileName = QtGui.QFileDialog.getOpenFileName(parent=None,
                                                     caption=caption,
                                                     directory=homeDir,
                                                     filter=yamlFilter)
        if isinstance(fileName, str):
            config = fileName  # string path to .yaml or .yml config file
        elif isinstance(fileName, tuple):
            try:
                config = fileName[0]
            except IndexError:
                print('No Config file found.')
                print('Please Select a directory with a .yaml file.')
                print('Loading Canceled ...')
                return
        else:
            print('No Config file found.')
            print('Please Select a directory with a .yaml file.')
            print('Loading Canceled ...')
            return
        if config == '':
            print("Loading canceled")
            return

        if self.exp is not None:
            # already loaded an experiment; save old experiment then load new
            self.prev_exp = self.exp

        self.exp = Experiment()
        # path_to_config = os.path.join(new_dir, config)
        self.exp.fromFile(config)
        print("New Data Path loaded from file: {}".format(self.exp.path))
        print("Loaded the following settings:")

        yaml.dump(self.exp.loaded_settings, stream=sys.stdout)

        if self.exp.exp_type == 'LEEM':
            self.load_LEEM_experiment()
        elif self.exp.exp_type == 'LEED':
            self.load_LEED_experiment()
        else:
            print("Error: Unrecognized Experiment Type in YAML Config file")
            print("Valid Experiment Types for LiveViewer are LEEM, LEED")
            print("Please refer to Experiment.yaml for documentation.")
            return

    def load_LEEM_experiment(self):
        """Load LEEM data from settings described by YAML config file."""
        if self.exp is None:
            return
        self.tabs.setCurrentIndex(0)
        if self.exp.data_type.lower() == 'raw':
            try:
                # use settings from self.sexp
                self.thread = WorkerThread(task='LOAD_LEEM',
                                           path=str(self.exp.path),
                                           imht=self.exp.imh,
                                           imwd=self.exp.imw,
                                           bits=self.exp.bit,
                                           byte=self.exp.byte_order)
                try:
                    self.thread.disconnect()
                except TypeError:
                    pass  # no signals connected, that's OK, continue as needed
                self.thread.connectOutputSignal(self.retrieve_LEEM_data)
                self.thread.finished.connect(self.update_LEEM_img_after_load)
                self.thread.start()
            except ValueError:
                print("Error loading LEEM Experiment:")
                print("Please Verify Experiment Config Settings.")
                return

        elif self.exp.data_type.lower() == 'image':
            try:
                self.thread = WorkerThread(task='LOAD_LEEM_IMAGES',
                                           path=self.exp.path,
                                           ext=self.exp.ext)
                try:
                    self.thread.disconnect()
                except TypeError:
                    pass  # no signals connected, that's OK, continue as needed
                self.thread.connectOutputSignal(self.retrieve_LEEM_data)
                self.thread.finished.connect(self.update_LEEM_img_after_load)
                self.thread.start()
            except ValueError:
                print('Error loading LEEM data from images.')
                print('Please check YAML experiment config file')
                print('Required parameters: path, ext')
                print('Check for valid data path')
                print('Check file extensions: \'.tif\' and \'.png\'.')
                return

    def load_LEED_experiment(self):
        """Load LEED data from settings described by YAML config file."""
        if self.exp is None:
            return
        self.tabs.setCurrentIndex(1)

        if self.hasdisplayedLEEDdata:
            # self.LEEDimageplotwidget.getPlotItem().clear()
            self.LEEDivplotwidget.getPlotItem().clear()
        if self.exp.data_type.lower() == 'raw':
            try:
                # use settings from self.exp
                self.thread = WorkerThread(task='LOAD_LEED',
                                           path=str(self.exp.path),
                                           imht=self.exp.imh,
                                           imwd=self.exp.imw,
                                           bits=self.exp.bit,
                                           byte=self.exp.byte_order)
                try:
                    self.thread.disconnect()
                except TypeError:
                    # no signal connections - this is OK
                    pass
                self.thread.connectOutputSignal(self.retrieve_LEED_data)
                self.thread.finished.connect(self.update_LEED_img_after_load)
                self.thread.start()
            except ValueError:
                print('Error Loading LEED Data: Please Recheck YAML Settings')
                return

        elif self.exp.data_type.lower() == 'image':
            try:
                self.thread = WorkerThread(task='LOAD_LEED_IMAGES',
                                           ext=self.exp.ext,
                                           path=self.exp.path,
                                           byte=self.exp.byte_order)
                try:
                    self.thread.disconnect()
                except TypeError:
                    # no signals were connected - this is OK
                    pass
                self.thread.connectOutputSignal(self.retrieve_LEED_data)
                self.thread.finished.connect(self.update_LEED_img_after_load)
                self.thread.start()
            except ValueError:
                print('Error Loading LEED Experiment from image files.')
                print('Please Check YAML settings in experiment config file')
                print('Required parameters: data path and data extension.')
                print('Valid data extenstions: \'.tif\', \'.png\', \'.jpg\'')
                return

    def outputIV(self, datatype=None):
        """Output current I(V) plots as tab delimited text files.

        :param: datatype- String desginating either 'LEEM' or 'LEED' data to output
        """
        if datatype is None:
            return
        elif datatype == 'LEEM' and self.hasdisplayedLEEMdata and self.LEEMselections:
            outdir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Directory",
                                                                options=QtWidgets.QFileDialog.ShowDirsOnly)
            try:
                outdir = outdir[0]
            except IndexError:
                print("Error selecting output file directory.")
                return
            outdir = str(outdir)  # cast from QString to string

            # Query User for output file name
            msg = "Enter name for output file(s)."
            outname = QtWidgets.QFileDialog.getSaveFileName(self, msg)

            try:
                outname = outname[0]
            except IndexError:
                print("Error getting output file name.")
                return
            outname = str(outname)  # cast from QString ot string

            outfile = os.path.join(outdir, outname)
            if self.threads:
                # there are still thread objects in the container
                for thread in self.threads:
                    if not thread.isFinished():
                        print("Error: One or more threads has not finished file I/O ...")
                        return
            self.threads = []
            for idx, tup in enumerate(self.LEEMselections):
                outfile = os.path.join(outdir, outname+str(idx)+'.txt')
                x = tup[0]
                y = tup[1]
                ilist = self.leemdat.dat3d[y, x, :]
                if self.smoothLEEMoutput:
                    ilist = LF.smooth(ilist,
                                      window_len=self.LEEMWindowLen,
                                      window_type=self.LEEMWindowType)
                thread = WorkerThread(task='OUTPUT_TO_TEXT',
                                           elist=self.leemdat.elist,
                                           ilist=ilist,
                                           name=outfile)
                thread.finished.connect(self.output_complete)
                self.threads.append(thread)
                thread.start()

        elif datatype == 'LEED' and self.hasdisplayedLEEDdata and self.LEEDclickpos:
            # Query User for output directory
            # PyQt5 - This method now returns a tuple - we want only the first element
            outdir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Directory",
                                                                options=QtWidgets.QFileDialog.ShowDirsOnly)
            try:
                outdir = outdir[0]
            except IndexError:
                print("Error selecting output file directory.")
                return
            outdir = str(outdir)  # cast from QString to string

            # Query User for output file name
            msg = "Enter name for output file(s)."
            outname = QtWidgets.QFileDialog.getSaveFileName(self, msg)

            try:
                outname = outname[0]
            except IndexError:
                print("Error getting output file name.")
                return
            outname = str(outname)  # cast from QString ot string

            outfile = os.path.join(outdir, outname)
            if self.threads:
                # there are still thread objects in the container
                for thread in self.threads:
                    if not thread.isFinished():
                        print("Error: One or more threads has not finished file I/O ...")
                        return
            self.threads = []
            if len(self.LEEDrects) != len(self.LEEDclickpos):
                print("Error: number of LEED widnows does not match number of Click coordinates.")
                return
            for idx, tup in enumerate(self.LEEDclickpos):
                outfile = os.path.join(outdir, outname+str(idx)+'.txt')
                rad = self.LEEDrects[idx][3]
                x = int(tup[0])
                y = int(tup[1])
                int_window = self.leeddat.dat3d[y - rad:y + rad + 1,
                                                x - rad:x + rad + 1, :]
                # get average intensity per window
                ilist = [img.sum()/(2*rad*2*rad) for img in np.rollaxis(int_window, 2)]
                if self.smoothLEEDoutput:
                    ilist = LF.smooth(ilist,
                                      window_len=self.LEEDWindowLen,
                                      window_type=self.LEEDWindowType)
                thread = WorkerThread(task='OUTPUT_TO_TEXT',
                                           elist=self.leeddat.elist,
                                           ilist=ilist,
                                           name=outfile)
                thread.finished.connect(self.output_complete)
                self.threads.append(thread)
                thread.start()

    def validate_smoothing_settings(self, but=None):
        """Validate User input from Config Tab smoothing settings."""
        if but is None:
            return
        elif but == 'LEED':
            window_type = str(self.smooth_LEED_window_type_menu.currentText())
            window_len = str(self.LEED_window_len_entry.text())
        elif but == 'LEEM':
            window_type = str(self.smooth_LEEM_window_type_menu.currentText())
            window_len = str(self.LEEM_window_len_entry.text())
        else:
            print("Error: Invalid button label passed to validate_smoothing_settings().")
            return
        print("Currently selected smoothing settings: {0} {1}".format(window_type, window_len))
        try:
            window_len = int(window_len)
        except TypeError:
            print("Error: Window Length setting must be entered as an even integer")
            return
        if window_len <= 0:
            print("Error: Window Length mut be positive even integer")
            return
        elif window_len % 2 != 0:
            print("Warning: Window Length was odd. Using next highest even integer")
            window_len += 1
        if window_type.lower() not in ['flat', 'hanning',
                                       'hamming', 'bartlett',
                                       'blackman']:
            print("Error: Invalid Window Type for data smoothing.")
            return
        if but == "LEED":
            self.LEEDWindowType = window_type.lower()
            self.LEEDWindowLen = window_len
        else:
            self.LEEMWindowType = window_type.lower()
            self.LEEMWindowLen = window_len
            # Changing the LEEM smoothing settings means we need to
            # reset our position mask array which declared if we had
            # previously calculated the smoothed data for a given point (x, y)
            if self.hasdisplayedLEEMdata:
                # if we haven't displayed data yet, don't bother with this step.
                self.leemdat.posMask.fill(0)
        return

    def toggleReflectivity(self, data=None):
        """Swap boolean flag for plotting Reflectivity instead of Intensity."""
        if data is None:
            return
        if data == "LEEM":
            self.rescaleLEEMIntensity = not self.rescaleLEEMIntensity
            self.LEEMivplotwidget.setLabel("left", "Reflectivity")
        if data == "LEED":
            pass  # TODO: decide if we want this as a feature

    def apply_LEED_window_size(self):
        """Set side length for Rectangular integration window from User input."""
        userinput = str(self.LEEDRectEntry.text())
        try:
            userinput = int(userinput)
        except TypeError:
            print("Error: LEED Window Side length must be entered as an even integer")
            return
        if userinput % 2 != 0:
            print("Warning: Window side Length was odd. Using next highest even integer")
            userinput += 1
        self.boxrad = userinput / 2
        print("Setting LEED Window size to {0}x{1} ...".format(userinput, userinput))
        return

    @QtCore.pyqtSlot()
    def smoothing_statechange(self, data=None):
        """Toggle LEED smoothing option."""
        if data is None:
            return
        elif data == 'LEED':
            if self.smoothLEEDCheckBox.isChecked():
                self.smoothLEEDplot = True
                self.smoothLEEDoutput = True
            else:
                self.smoothLEEDplot = False
                self.smoothLEEDoutput = False
            return
        elif data == 'LEEM':
            if self.smoothLEEMCheckBox.isChecked():
                self.smoothLEEMplot = True
                self.smoothLEEMoutput = True
            else:
                self.smoothLEEMplot = False
                self.smoothLEEMoutput = False
            return

    @staticmethod
    @QtCore.pyqtSlot()
    def output_complete():
        """Recieved a finished() SIGNAL from a QThread object."""
        print('File output successfully')

    @QtCore.pyqtSlot(np.ndarray)
    def retrieve_LEEM_data(self, data):
        """Grab the 3d numpy array emitted from the data loading I/O thread."""
        self.leemdat.dat3d = data
        self.leemdat.dat3ds = data.copy()
        self.leemdat.posMask = np.zeros((self.leemdat.dat3d.shape[0],
                                         self.leemdat.dat3d.shape[1]))
        # print("LEEM data recieved from QThread.")
        return

    @QtCore.pyqtSlot(np.ndarray)
    def retrieve_LEED_data(self, data):
        """Grab the numpy array emitted from the data loading I/O thread."""
        # data = [np.fliplr(np.rot90(np.rot90(img))) for img in np.rollaxis(data, 2)]
        # data = np.dstack(data)
        self.leeddat.dat3d = data
        self.leeddat.dat3ds = data.copy()
        self.leeddat.posMask = np.zeros((self.leeddat.dat3d.shape[0],
                                         self.leeddat.dat3d.shape[1]))

    @QtCore.pyqtSlot()
    def update_LEEM_img_after_load(self):
        """Called upon data loading I/O thread emitting finished signal."""
        # print("QThread has finished execution ...")

        # Check that data was actually loaded
        if self.leemdat.dat3d is None:
            return

        if self.hasdisplayedLEEMdata:
            self.LEEMimageplotwidget.getPlotItem().clear()

        self.curLEEMIndex = self.leemdat.dat3d.shape[2]//2

        # pyqtgraph displays the array rotated 90 degrees CCW. To force the display to match the original array we
        # display a rotated + flipped array so that the image is displayed correctly
        # see the following discussion on the pyqtgraph forum for more information
        # https://groups.google.com/forum/?utm_medium=email&utm_source=footer#!msg/pyqtgraph/aMQW16vF9Os/mmILDzCyCAAJ
        # Pyqtgraph interprets array data as [width, height]. So we apply a horizontal flip via [::-1, :]
        # then transpose the flipped array. This is equivalent to a 90 degree rotation in the CCW direction.

        self.LEEMimage = pg.ImageItem(self.leemdat.dat3d[::-1, :, self.curLEEMIndex].T)
        self.LEEMimageplotwidget.addItem(self.LEEMimage)
        self.LEEMimageplotwidget.hideAxis('bottom')
        self.LEEMimageplotwidget.hideAxis('left')

        # reset new crosshair on load to force crosshair on top of image
        self.crosshair = ExtendedCrossHair()
        self.LEEMimageplotwidget.addItem(self.crosshair.hline,
                                         ignoreBounds=True)
        self.LEEMimageplotwidget.addItem(self.crosshair.vline,
                                         ignoreBounds=True)

        self.leemdat.elist = [self.exp.mine]
        while len(self.leemdat.elist) < self.leemdat.dat3d.shape[2]:
            nextEnergy = self.leemdat.elist[-1] + self.exp.stepe
            self.leemdat.elist.append(round(nextEnergy, 2))
        self.checkDataSize(datatype="LEEM")
        self.hasdisplayedLEEMdata = True
        title = "Real Space LEEM Image: {} eV"
        energy = LF.filenumber_to_energy(self.leemdat.elist, self.curLEEMIndex)
        # self.LEEMimageplotwidget.setTitle(title.format(energy),
        #                                  **self.labelStyle)
        self.LEEMimtitle.setText(title.format(energy))
        self.LEEMimageplotwidget.setFocus()

    @QtCore.pyqtSlot()
    def update_LEED_img_after_load(self):
        """Called upon data loading I/O thread emitting finished signal."""
        # if self.hasdisplayedLEEDdata:
        #     self.LEEDimageplotwidget.getPlotItem().clear()

        # check that data was actually loaded
        if self.leeddat.dat3d is None:
            return

        self.curLEEDIndex = self.leeddat.dat3d.shape[2]//2

        # pyqtgraph displays the array rotated 90 degrees CCW. To force the display to match the original array we
        # display a rotated + flipped array so that the image is displayed correctly
        # see the following discussion on the pyqtgraph forum for more information
        # https://groups.google.com/forum/?utm_medium=email&utm_source=footer#!msg/pyqtgraph/aMQW16vF9Os/mmILDzCyCAAJ
        # Pyqtgraph interprets array data as [width, height]. So we apply a horizontal flip via [::-1, :]
        # then transpose the flipped array. This is equivalent to a 90 degree rotation in the CCW direction.

        self.LEEDimage = pg.ImageItem(self.leeddat.dat3d[::-1, :, self.curLEEDIndex].T)
        self.LEEDimagewidget.addItem(self.LEEDimage)
        self.LEEDimagewidget.hideAxis('bottom')
        self.LEEDimagewidget.hideAxis('left')

        self.leeddat.elist = [self.exp.mine]
        while len(self.leeddat.elist) < self.leeddat.dat3d.shape[2]:
            newEnergy = self.leeddat.elist[-1] + self.exp.stepe
            self.leeddat.elist.append(round(newEnergy, 2))
        self.hasdisplayedLEEDdata = True
        title = "Reciprocal Space LEED Image: {} eV"
        energy = LF.filenumber_to_energy(self.leeddat.elist, self.curLEEDIndex)
        self.LEEDTitle.setText(title.format(energy))

    def checkDataSize(self, datatype=None):
        """Ensure helper array sizes all match main data array size."""
        if datatype is None:
            return
        elif datatype == 'LEEM':
            mainshape = self.leemdat.dat3d.shape
            if self.leemdat.dat3ds.shape != mainshape:
                self.leemdat.dat3ds = np.zeros(mainshape)
            if self.leemdat.posMask.shape != (mainshape[0], mainshape[1]):
                self.leemdat.posMask = np.zeros((mainshape[0], mainshape[1]))
        elif datatype == 'LEED':
            pass
        else:
            return

    def enableLEEMWindow(self):
        """Enable I(V) extraction from rectangular window.

        Default is single pixel extraction.
        """
        # disable mouse movement tracking
        # reroute mouse click signal to new handle
        try:
            self.sigmmvLEEM.disconnect()
        except:
            # If sigmvLEEM is not connected to anything, an exception is raised
            # This is ok. Here we just want to disable mousemovement tracking
            pass
        try:
            self.sigmcLEEM.disconnect()
        except:
            # If sigmvLEEM is not connected to anything, an exception is raised
            # This is ok. Here we just want to disable the default mouse click behaviour
            pass

        self.sigmcLEEM.connect(self.handleLEEMWindow)

        # move cropsshair away from image area
        self.crosshair.vline.setPos(0)
        self.crosshair.hline.setPos(0)

        # remove any ucrrent LEEM clicks
        self.LEEMclicks = 0
        if self.LEEMcircs:
            for circ in self.LEEMcircs:
                self.LEEMimageplotwidget.scene().removeItem(circ)
        self.LEEMcircs = []
        self.LEEMselections = []
        self.LEEMRectCount = 0
        self.LEEMRects = []

        self.LEEMRectWindowEnabled = True
        self.parentWidget().extractLEEMWindowAction.setEnabled(True)

    def disableLEEMWindow(self):
        """Disable I(V) extraction from rectangular window.

        Reinstate default behavior: single pixel extraction.
        """
        try:
            self.sigmmvLEEM.disconnect()
        except:
            # If sigmvLEEM is not connected to anything, an exception is raised
            # This is ok, and we can continue to reconnect this signal to the
            # LEEM mouse movement tracking handler
            pass
        try:
            self.sigmcLEEM.disconnect()
        except:
            # If sigmvLEEM is not connected to anything, an exception is raised
            # This is ok, and we can continue to reconnect this signal to the
            # LEEM mouse click handler
            pass

        # delete current rect windows and reset click count
        for tup in self.LEEMRects:
            self.LEEMimageplotwidget.scene().removeItem(tup[0])
        self.LEEMclicks = 0
        self.LEEMcircs = []
        self.LEEMselections = []
        self.LEEMRectCount = 0
        self.LEEMRects = []
        # Reset Mouse event signals to default behaviour
        self.sigmcLEEM.connect(self.handleLEEMClick)
        self.sigmmvLEEM.connect(self.handleLEEMMouseMoved)
        self.LEEMRectWindowEnabled = False
        self.parentWidget().extractLEEMWindowAction.setEnabled(False)

    def handleLEEMWindow(self, event):
        """Use mouse mouse clicks to generate rectangular window for I(V) extraction."""
        if not self.hasdisplayedLEEMdata or event.currentItem is None or event.button() == 2:
            return
        if len(self.qcolors) <= len(self.LEEMRects):
            print("Maximum number of LEEM Selections reached. Please clear current selection.")
            return

        if self.LEEMclicks == 0:
            # this was the first click

            brush = QtGui.QBrush(self.qcolors[len(self.LEEMRects)])
            pos = event.pos()
            rad = 8
            # account for offset in patch location from QRectF
            x = pos.x() - rad/2
            y = pos.y() - rad/2
            # create circular patch
            circ = self.LEEMimageplotwidget.scene().addEllipse(x, y, rad, rad, brush=brush)
            self.LEEMcircs.append(circ)
            self.firstclick = (x, y)  # position of center of patch for first clicks
            # mapped coordinates for first click:
            vb = self.LEEMimageplotwidget.getPlotItem().getViewBox()
            mappedclick = vb.mapSceneToView(event.scenePos())
            xmp = int(mappedclick.x())
            ymp = self.leemdat.dat3d.shape[0] - 1 - int(mappedclick.y())
            self.firstclickmap = (xmp, ymp)  # location of first click in array coordinates
            self.LEEMclicks += 1
            return

        elif self.LEEMclicks == 1:
            # this is the second click
            self.secondclick = (event.pos().x(), event.pos().y())
            vb = self.LEEMimageplotwidget.getPlotItem().getViewBox()
            mappedclick = vb.mapSceneToView(event.scenePos())
            xmp = int(mappedclick.x())
            ymp = self.leemdat.dat3d.shape[0] - 1 - int(mappedclick.y())
            self.secondclickmap = (xmp, ymp)  # location of second click in array coordinates

            rectcoords = LF.getRectCorners(self.firstclick, self.secondclick)
            rectcoordsmap = LF.getRectCorners(self.firstclickmap, self.secondclickmap)
            topleft = rectcoords[0]  # scene coordinates
            topleftmap = rectcoordsmap[0]  # array coordinates
            bottomright = rectcoords[1]  # scene coordinates
            bottomrightmap = rectcoordsmap[1] # array coordinates
            width = bottomright[0] - topleft[0]
            height = bottomright[1] - topleft[1]
            rect = QtCore.QRectF(topleft[0], topleft[1], width, height)
            self.LEEMRectCount += 1
            pen = QtGui.QPen()
            pen.setStyle(QtCore.Qt.SolidLine)
            pen.setWidth(4)
            # pen.setBrush(QtCore.Qt.red)
            pen.setColor(self.qcolors[self.LEEMRectCount - 1])
            rectitem = self.LEEMimageplotwidget.scene().addRect(rect, pen=pen)
            self.LEEMRects.append((rectitem, rect, pen, topleftmap, bottomrightmap))
            self.LEEMclicks = 0
            for circ in self.LEEMcircs:
                self.LEEMimageplotwidget.scene().removeItem(circ)
            self.LEEMcircs = []

    def extractLEEMWindows(self):
        """Extract I(V) from User defined rectangular windows and Plot in main IV area."""
        if not self.hasdisplayedLEEMdata or not self.LEEMRects or self.LEEMRectCount == 0:
            return
        self.LEEMivplotwidget.clear()
        for tup in self.LEEMRects:
            topleft = tup[3]
            bottomright = tup[4]
            xtl = int(topleft[0])
            ytl = int(topleft[1])
            width = int(bottomright[0] - xtl)
            height = int(bottomright[1] - ytl)
            print("Topleft: {}".format(topleft))
            print("Bottomright: {}".format(bottomright))
            print("Window Selected: x={0}, y={1}, width={2}, height={3}".format(xtl, ytl, width, height))
            window = self.leemdat.dat3d[ytl:ytl + height + 1,
                                        xtl:xtl + width + 1, :]
            ilist = [img.sum()/(width*height) for img in np.rollaxis(window, 2)]
            if self.smoothLEEMplot:
                ilist = LF.smooth(ilist, window_len=self.LEEMWindowLen, window_type=self.LEEMWindowType)
            self.LEEMivplotwidget.plot(self.leemdat.elist, ilist, pen=pg.mkPen(tup[2].color(), width=2))

    def handleLEEMClick(self, event):
        """User click registered in LEEMimage area.

        Handles offset for QRectF drawn for circular patch to ensure that
        the circle is drawn directly below the mouse pointer.

        Appends I(V) curve from clicked location to alternate plot window so
        as to not interfere with the live tracking plot.
        """
        if not self.hasdisplayedLEEMdata:
            return

        # clicking outside image area may cause event.currentItem
        # to be None. This would then raise an error when trying to
        # call event.pos()
        if event.currentItem is None:
            return

        if len(self.qcolors) <= self.LEEMclicks:
            print("Maximum number of LEEM selections. Please clear current selections.")
            return
        self.LEEMclicks += 1

        pos = event.pos()
        mappedPos = self.LEEMimage.mapFromScene(pos)
        xmapfs = int(mappedPos.x())
        ymapfs = int(mappedPos.y())

        if xmapfs < 0 or \
           xmapfs > self.leemdat.dat3d.shape[1] or \
           ymapfs < 0 or \
           ymapfs > self.leemdat.dat3d.shape[0]:
            return  # discard click events originating outside the image

        if self.currentLEEMPos is not None:
            try:
                # mouse position
                xmp = self.currentLEEMPos[0]
                ymp = self.currentLEEMPos[1]  # x and y in array coordinates (top edge is y=0)
            except IndexError:
                return
        else:
            print("Error: Failed to get currentLEEMPos for LEEMClick().")
            return
        xdata = self.leemdat.elist
        ydata = self.leemdat.dat3d[ymp, xmp, :]
        if self.smoothLEEMplot:
            ydata = LF.smooth(ydata, window_len=self.LEEMWindowLen, window_type=self.LEEMWindowType)

        brush = QtGui.QBrush(self.qcolors[self.LEEMclicks - 1])
        rad = 8
        x = pos.x() - rad/2  # offset for QRectF
        y = pos.y() - rad/2  # offset for QRectF

        circ = self.LEEMimageplotwidget.scene().addEllipse(x, y, rad, rad, brush=brush)
        # print("Click at x={0}, y={1}".format(x, y))
        self.LEEMcircs.append(circ)
        self.LEEMselections.append((xmp, ymp))  # (x, y format)

        pen = pg.mkPen(self.qcolors[self.LEEMclicks - 1], width=2)
        pdi = pg.PlotDataItem(xdata, ydata, pen=pen)
        self.staticLEEMplot.addItem(pdi)
        self.staticLEEMplot.setTitle("LEEM-I(V)")
        self.staticLEEMplot.setLabel('bottom', 'Energy', units='eV', **self.labelStyle)
        self.staticLEEMplot.setLabel('left', 'Intensity', units='a.u.', **self.labelStyle)
        if not self.staticLEEMplot.isVisible():
            self.staticLEEMplot.show()

    def handleLEEMMouseMoved(self, pos):
        """Track mouse movement within LEEM image area and display I(V) from mouse location."""
        if not self.hasdisplayedLEEMdata:
            return
        if isinstance(pos, tuple):
            try:
                # if pos a tuple containing a QPointF object
                pos = pos[0]
            except IndexError:
                # empty tuple
                return
        # else pos is a QPointF object which can be mapped directly

        mappedPos = self.LEEMimage.mapFromScene(pos)
        xmp = int(mappedPos.x())
        ymp = int(mappedPos.y())
        if xmp < 0 or \
           xmp > self.leemdat.dat3d.shape[1] - 1 or \
           ymp < 0 or \
           ymp > self.leemdat.dat3d.shape[0] - 1:
            return  # discard  movement events originating outside the image

        # update crosshair
        self.crosshair.curPos = (xmp, ymp)  # place cross hair with y coordinate in reference to bottom edge as y=0
        self.crosshair.vline.setPos(xmp)
        self.crosshair.hline.setPos(ymp)

        # convert to array (numpy) y coordinate by inverting the y value
        ymp = self.leemdat.dat3d.shape[0] - 1 - ymp
        self.currentLEEMPos = (xmp, ymp)  # used for handleLEEMClick()
        # print("Mouse moved to: {0}, {1}".format(xmp, ymp))  # array coordinates

        # update IV plot
        xdata = self.leemdat.elist
        ydata = self.leemdat.dat3d[ymp, xmp, :]  # raw unsmoothed data

        if self.rescaleLEEMIntensity:
            ydata = [point/float(max(ydata)) for point in ydata]
        if self.smoothLEEMplot and not self.leemdat.posMask[ymp, xmp]:
            # We want to plot smoothed dat but the I(V) of the current pixel position
            # has not yet been smoothed
            ydata = LF.smooth(ydata, window_type=self.LEEMWindowType, window_len=self.LEEMWindowLen)
            self.leemdat.dat3ds[ymp, xmp, :] = ydata
            self.leemdat.posMask[ymp, xmp] = 1

        elif self.smoothLEEMplot and self.leemdat.posMask[ymp, xmp]:
            # We want to plot smoothed data and have already calculated it for this pixel position
            ydata = self.leemdat.dat3ds[ymp, xmp, :]

        pen = pg.mkPen(self.qcolors[0], width=3)
        pdi = pg.PlotDataItem(xdata, ydata, pen=pen)
        self.LEEMivplotwidget.getPlotItem().clear()
        self.LEEMivplotwidget.getPlotItem().addItem(pdi, clear=True)

    def handleLEEDClick(self, event):
        """User click registered in LEEDimage area."""
        if not self.hasdisplayedLEEDdata or event.currentItem is None:
            return

        # Ensure number of LEED windows remains less than the max colors
        if len(self.qcolors) <= self.LEEDclicks:
            print("Maximum number of LEED Windows Reached. Please clear current selections.")
            return

        self.LEEDclicks += 1
        pos = event.pos()  # scene position
        x = int(pos.x())
        y = int(pos.y())

        viewbox = self.LEEDimagewidget.getPlotItem().getViewBox()
        mappedPos = viewbox.mapSceneToView(event.scenePos())  # position in array coordinates
        xmp = int(mappedPos.x())
        ymp = int(mappedPos.y())

        # pyqtgraph uses bottom edge as y=0; this converts the coordinate to the numpy system
        ymp = (self.leeddat.dat3d.shape[0] - 1) - ymp

        # check to see if click is too close to edge
        if (xmp - self.boxrad < 0 or xmp + self.boxrad >= self.leeddat.dat3d.shape[1] or
           ymp - self.boxrad < 0 or ymp + self.boxrad >= self.leeddat.dat3d.shape[0]):
            print("Error: Click registered too close to image edge.")
            print("Reduce window size or choose alternate extraction point")
            self.LEEDclicks -= 1
            return

        if xmp >= 0 and xmp < self.leeddat.dat3d.shape[1] - 1 and \
           ymp >= 0 and ymp < self.leeddat.dat3d.shape[0] - 1:
            # valid array coordinates

            # QGraphicsRectItem is drawn using the scene coordinates (x, y)
            topleftcorner = QtCore.QPointF(x - self.boxrad,
                                           y - self.boxrad)
            rect = QtCore.QRectF(topleftcorner.x(), topleftcorner.y(),
                                 2*self.boxrad, 2*self.boxrad)
            pen = QtGui.QPen()
            pen.setStyle(QtCore.Qt.SolidLine)
            pen.setWidth(4)
            # pen.setBrush(QtCore.Qt.red)
            pen.setColor(self.qcolors[self.LEEDclicks - 1])
            rectitem = self.LEEDimage.scene().addRect(rect, pen=pen)  # QGraphicsRectItem

            # We need access to the QGraphicsRectItem inorder to later call
            # removeItem(). However, we also need access to the QRectF object
            # in order to get coordinates. Thus we store a reference to both along
            # with the pen used for coloring the Rect.
            # Finally, we need to keep track of the window side length for each selections
            # as it is user configurable
            self.LEEDrects.append((rectitem, rect, pen, self.boxrad))
            self.LEEDclickpos.append((xmp, ymp))  # store x, y coordinate of mouse click in array coordinates
            # print("Click registered at array coordinates: x={0}, y={1}".format(xmp, ymp))

    def processLEEDIV(self):
        """Plot I(V) from User selections."""
        if not self.hasdisplayedLEEDdata or not self.LEEDrects or not self.LEEDclickpos:
            return
        if len(self.LEEDrects) != len(self.LEEDclickpos):
            print("Error: Number of LEED widnows does not match number of stored click positions")
            return
        for idx, tup in enumerate(self.LEEDclickpos):
            # center coordinates
            xc = tup[0]
            yc = tup[1]

            # the lengths of LEEDclickpos and LEEDrects are ensured to be equal now
            rad = int(self.LEEDrects[idx][3])  # cast to int to ensure array indexing uses ints

            # top left corner in array coordinates
            xtl = xc - rad
            ytl = yc - rad

            int_window = self.leeddat.dat3d[ytl:ytl + 2*rad + 1,
                                            xtl:xtl + 2*rad + 1, :]
            # store average intensity per window
            ilist = [img.sum()/(2*rad*2*rad) for img in np.rollaxis(int_window, 2)]
            # ilist = [img.sum() for img in np.rollaxis(int_window, 2)]
            if self.smoothLEEDplot:
                ilist = LF.smooth(ilist, window_type=self.LEEDWindowType, window_len=self.LEEDWindowLen)
            self.LEEDivplotwidget.plot(self.leeddat.elist, ilist, pen=pg.mkPen(self.qcolors[idx], width=3))

    def clearLEEDIV(self):
        """Triggered by menu action to clear all LEED selections."""
        self.LEEDivplotwidget.clear()
        if self.LEEDrects:
            # items stored as (QRectF, QPen)
            for tup in self.LEEDrects:
                self.LEEDimagewidget.scene().removeItem(tup[0])
            self.LEEDrects = []
            self.LEEDclickpos = []
            self.LEEDclicks = 0
            self.LEEDclickpos = []

    def clearLEEMIV(self):
        """Clear User selections from LEEM image and clear IV plot."""
        if self.LEEMcircs:
            for item in self.LEEMcircs:
                self.LEEMimageplotwidget.scene().removeItem(item)
        self.staticLEEMplot.clear()
        if self.staticLEEMplot.isVisible():
            self.staticLEEMplot.close()
            self.staticLEEMplot = pg.PlotWidget()  # reset to new plot instance but don't call show()
            self.staticLEEMplot.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.LEEMclicks = 0
        self.LEEMselections = []
        self.LEEMcircs = []

    def clearLEEMWindows(self):
        """Clear LEEM rectangular windows."""
        for tup in self.LEEMRects:
            # first item in container is rectitem
            self.LEEMimageplotwidget.scene().removeItem(tup[0])
        for circ in self.LEEMcircs:
            self.LEEMimageplotwidget.scene().removeItem(circ)
        self.LEEMivplotwidget.clear()
        self.LEEMclicks = 0
        self.LEEMcircs = []
        self.LEEMselections = []
        self.LEEMRectCount = 0
        self.LEEMRects = []

    def keyPressEvent(self, event):
        """Set Arrow keys for navigation."""
        # LEEM Tab is active
        if self.tabs.currentIndex() == 0 and \
           self.hasdisplayedLEEMdata:
            # handle LEEM navigation
            maxIdx = self.leemdat.dat3d.shape[2] - 1
            minIdx = 0
            if (event.key() == QtCore.Qt.Key_Left) and \
               (self.curLEEMIndex >= minIdx + 1):
                self.curLEEMIndex -= 1
                self.showLEEMImage(self.curLEEMIndex)
                title = "Real Space LEEM Image: {} eV"
                energy = LF.filenumber_to_energy(self.leemdat.elist,
                                                 self.curLEEMIndex)
                # self.LEEMimageplotwidget.setTitle(title.format(energy))
                self.LEEMimtitle.setText(title.format(energy))
            elif (event.key() == QtCore.Qt.Key_Right) and \
                 (self.curLEEMIndex <= maxIdx - 1):
                self.curLEEMIndex += 1
                self.showLEEMImage(self.curLEEMIndex)
                title = "Real Space LEEM Image: {} eV"
                energy = LF.filenumber_to_energy(self.leemdat.elist,
                                                 self.curLEEMIndex)
                # self.LEEMimageplotwidget.setTitle(title.format(energy))
                self.LEEMimtitle.setText(title.format(energy))
        # LEED Tab is active
        elif (self.tabs.currentIndex() == 1) and \
             (self.hasdisplayedLEEDdata):
            # handle LEED navigation
            maxIdx = self.leeddat.dat3d.shape[2] - 1
            minIdx = 0
            if (event.key() == QtCore.Qt.Key_Left) and \
               (self.curLEEDIndex >= minIdx + 1):
                self.curLEEDIndex -= 1

                self.showLEEDImage(self.curLEEDIndex)

                title = "Reciprocal Space LEED Image: {} eV"
                energy = LF.filenumber_to_energy(self.leeddat.elist,
                                                 self.curLEEDIndex)
                self.LEEDTitle.setText(title.format(energy))
            elif (event.key() == QtCore.Qt.Key_Right) and \
                 (self.curLEEDIndex <= maxIdx - 1):
                self.curLEEDIndex += 1

                self.showLEEDImage(self.curLEEDIndex)

                title = "Reciprocal Space LEED Image: {} eV"
                energy = LF.filenumber_to_energy(self.leeddat.elist,
                                                 self.curLEEDIndex)
                self.LEEDTitle.setText(title.format(energy))

    def showLEEMImage(self, idx):
        """Display LEEM image from main data array at index=idx."""
        if idx not in range(self.leemdat.dat3d.shape[2] - 1):
            return

        # see note in instance method update_LEEM_img_after_load()
        # for why the displayed image uses a horizontal flip + transpose
        self.LEEMimage.setImage(self.leemdat.dat3d[::-1, :, idx].T)

    def showLEEDImage(self, idx):
        """Display LEED image from main data array at index=idx."""
        if idx not in range(self.leeddat.dat3d.shape[2] - 1):
            return

        # see note in instance method update_LEED_img_after_load()
        # for why the displayed image uses a horizontal flip + transpose
        self.LEEDimage.setImage(self.leeddat.dat3d[::-1, :, idx].T)
