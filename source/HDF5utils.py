"""
PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: August, 2017
HDF5utils.py
Collection of utility methods and classes for working with HDF5 data
"""

import h5py
import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets


class HDF5ExpSettingsWidget(QtWidgets.QWidget):
    """Widget to get user input for exp settings to store in HDF5 Dataset attributes."""

    output_settings_signal = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        """Init view."""
        super(QtWidgets.QWidget, self).__init__(parent)
        self.setWindowTitle("Enter Experiment Settings")
        self.layout = QtWidgets.QVBoxLayout()
        self.initUI()

    def initUI(self):
        """Setup layout."""
        # Dataset name
        self.name_label = QtWidgets.QLabel("Enter name for HDF5 Dataset")
        name_hbox = QtWidgets.QHBoxLayout()
        name_hbox.addWidget(self.name_label)
        name_hbox.addStretch()
        self.name_input = QtWidgets.QLineEdit()
        name_hbox.addWidget(self.name_input)
        self.layout.addLayout(name_hbox)
        self.layout.addWidget(h_line())

        # Exp type settings
        self.exp_type_label = QtWidgets.QLabel("Exp. Type:")
        type_label_hbox = QtWidgets.QHBoxLayout()
        type_label_hbox.addStretch()
        type_label_hbox.addWidget(self.exp_type_label)
        type_label_hbox.addStretch()

        type_vbox = QtWidgets.QVBoxLayout()
        type_vbox.addLayout(type_label_hbox)

        self.type_menu = QtWidgets.QComboBox()
        self.type_menu.addItem("LEED")
        self.type_menu.addItem("LEEM")
        self.type_menu.addItem("PEEM")

        type_menu_hbox = QtWidgets.QHBoxLayout()
        type_menu_hbox.addStretch()
        type_menu_hbox.addWidget(self.type_menu)
        type_menu_hbox.addStretch()
        type_vbox.addLayout(type_menu_hbox)

        self.layout.addLayout(type_vbox)
        self.layout.addWidget(h_line())

        # Energy and time settings
        energy_time_hbox = QtWidgets.QHBoxLayout()

        time_settings_vbox = QtWidgets.QVBoxLayout()

        time_series_hbox = QtWidgets.QHBoxLayout()
        self.time_series_label = QtWidgets.QLabel("Time Series")
        self.time_series_checkbox = QtWidgets.QCheckBox()
        time_series_hbox.addWidget(self.time_series_label)
        time_series_hbox.addStretch()
        time_series_hbox.addWidget(self.time_series_checkbox)
        time_settings_vbox.addLayout(time_series_hbox)

        time_step_hbox = QtWidgets.QHBoxLayout()
        self.time_step_label = QtWidgets.QLabel("Time Step")
        self.time_step_input = QtWidgets.QLineEdit()
        time_step_hbox.addWidget(self.time_step_label)
        time_step_hbox.addStretch()
        time_step_hbox.addWidget(self.time_step_input)
        time_settings_vbox.addLayout(time_step_hbox)

        # enable Time Step LineEdit only if Time Series Checkbox is active
        self.time_step_input.setReadOnly(self.time_series_checkbox.checkState() == QtCore.Qt.Unchecked)
        sig = self.time_series_checkbox.stateChanged
        sig.connect(lambda state: self.time_step_input.setReadOnly(state == QtCore.Qt.Unchecked))

        energy_time_hbox.addLayout(time_settings_vbox)
        energy_time_hbox.addStretch()

        energy_vbox = QtWidgets.QVBoxLayout()
        self.energy_settings_label = QtWidgets.QLabel("Energy Settings:")
        energy_vbox.addWidget(self.energy_settings_label)

        energy_label_vbox = QtWidgets.QVBoxLayout()
        energy_input_vbox = QtWidgets.QVBoxLayout()

        energy_label_vbox.addWidget(QtWidgets.QLabel("min"))
        energy_label_vbox.addWidget(QtWidgets.QLabel("max"))
        energy_label_vbox.addWidget(QtWidgets.QLabel("step"))

        column_hbox = QtWidgets.QHBoxLayout()
        column_hbox.addLayout(energy_label_vbox)
        column_hbox.addStretch()

        self.min_energy_input = QtWidgets.QLineEdit()
        self.max_energy_input = QtWidgets.QLineEdit()
        self.step_energy_input = QtWidgets.QLineEdit()
        energy_input_vbox.addWidget(self.min_energy_input)
        energy_input_vbox.addWidget(self.max_energy_input)
        energy_input_vbox.addWidget(self.step_energy_input)

        column_hbox.addLayout(energy_input_vbox)

        energy_vbox.addLayout(column_hbox)
        energy_time_hbox.addLayout(energy_vbox)
        self.layout.addLayout(energy_time_hbox)
        self.layout.addStretch()
        self.layout.addWidget(h_line())

        # Buttons
        button_hbox = QtWidgets.QHBoxLayout()
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.done_button = QtWidgets.QPushButton("Done", self)
        button_hbox.addWidget(self.cancel_button)
        button_hbox.addStretch()
        button_hbox.addWidget(self.done_button)

        self.cancel_button.clicked.connect(lambda: self.close())
        self.done_button.clicked.connect(self.validateInput)
        self.layout.addLayout(button_hbox)

        self.setLayout(self.layout)

    def validateInput(self):
        """Ensure valid user input."""
        exp_type_selection = self.type_menu.currentText()
        is_time_series = self.time_series_checkbox.isChecked()
        if is_time_series:
            time_step = self.time_step_input.text()
            try:
                time_step = float(time_step)
            except ValueError:
                print("Error: Time Step must be input as a positive single decimal floating point.  ex: 0.1 ")
                return
            if time_step <= 0:
                print("Error: Time Step must be input as a positive single decimal floating point.  ex: 0.1 ")
                return
            # for time series data we do not require energy settings
            data_settings = {"Time Series": is_time_series,
                             "Time Step": time_step}
            self.output_settings_signal.emit(data_settings)
            self.close()
            return
        min_energy = self.min_energy_input.text()
        try:
            min_energy = float(min_energy)
        except ValueError:
            print("Error: Minimum energy must be input as a single decimal floating point.  ex: 0.1 ")
            return

        max_energy = self.max_energy_input.text()
        try:
            max_energy = float(max_energy)
        except ValueError:
            print("Error: Maximum energy must be input as a single decimal floating point.  ex: 0.1 ")
            return

        step_energy = self.step_energy_input.text()
        try:
            step_energy = float(step_energy)
        except ValueError:
            print("Error: Step energy must be input as a positive single decimal floating point.  ex: 0.1 ")
            return
        if step_energy <= 0:
            print("Error: Step energy must be input as a positive single decimal floating point.  ex: 0.1 ")
            return
        data_Settings = {"Time Series": is_time_series,
                         "Min Energy": min_energy,
                         "Max Energy": max_energy,
                         "Step Energy": step_energy}
        self.output_settings_signal.emit(data_Settings)
        self.close()
        return


class HDF5Viewer(QtWidgets.QWidget):
    """Container for QTreeView populated from HDF5."""

    output_array_signal = QtCore.pyqtSignal(np.ndarray)
    output_array_attrs_signal = QtCore.pyqtSignal(object)
    output_group_path_signal = QtCore.pyqtSignal(str)

    def __init__(self, model, allow_group_selection=False, parent=None):
        """Init view and set model."""
        super().__init__(parent)
        self.group = allow_group_selection
        self.treeview = QtWidgets.QTreeView()
        self.setWindowTitle("HDF5 File Explorer")
        self.treeview.setHeaderHidden(True)
        self.model = model
        self.treeview.setModel(model)
        self.initLayout()
        self.show()

    def initLayout(self):
        """Setup widget layout."""
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.treeview)

        self.button_hbox = QtWidgets.QHBoxLayout()

        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.close)
        self.select_button = QtWidgets.QPushButton("Select", self)
        self.select_button.clicked.connect(lambda: self.validateSelection(allow_group_selection=self.group))

        self.button_hbox.addWidget(self.cancel_button)
        self.button_hbox.addStretch()
        self.button_hbox.addWidget(self.select_button)

        self.layout.addLayout(self.button_hbox)

        self.setLayout(self.layout)

    def validateSelection(self, allow_group_selection=False):
        """Confirm that the current USER selection from the TreeView corresponds to an HDF5 Dataset.

        If the selection is valid, pass the selection paramters to HDF5ToArray()
        This will then provide a Numpy array to be returned for laoding into the main GUI.
        Adapted from Qt docs Model/View Tutorial "Working with Selections"

        :parameter allow_group_selection: bool indicating if it is ok to select a HDF5 Group instead of Dataset
        """
        # Recursively climb tree heirarchy and assemble path from root to current node
        path = []
        current_item_index = self.treeview.selectionModel().currentIndex()
        current_node = QtCore.QModelIndex(current_item_index)
        path.append(str(current_node.data(QtCore.Qt.DisplayRole)))

        # Note: rootnode has QModelIndex() as its parent
        while current_node.parent() != QtCore.QModelIndex():
            current_node = current_node.parent()
            path.append(str(current_node.data(QtCore.Qt.DisplayRole)))

        user_selected_tree_path = "/".join(reversed(path))  # Path from root to selected node
        print("Selected path to data: {}".format(user_selected_tree_path))

        # check HDF5 file if user selected path is valid
        valid_selection = self.model.validatePath(user_selected_tree_path)
        if not valid_selection:
            print("Error: {0} is not a valid path in HDF5 file {1}".format(user_selected_tree_path,
                                                                           self.model.hfile_path))
            return

        # If we just want to select a valid Group simply check validity and emit the Group path then return
        hfile = h5py.File(self.model.hfile_path, "r")
        if allow_group_selection:
            if isinstance(hfile[user_selected_tree_path], h5py._hl.group.Group):
                self.output_group_path_signal.emit(user_selected_tree_path)
                return
        hfile.close()

        # From here on we assume that we need to select data from a given HDF5 Dataset.
        data = HDF5ToArray(hfile_path=self.model.hfile_path,
                           hdf5_path_to_data=user_selected_tree_path)
        if data is None:
            # Problem with User selection; no np.ndarray returned
            return
        try:
            # Search User selected HDF5 Dataset for experiment configuration attributes
            hfile = h5py.File(self.model.hfile_path, "r")
            dataset = hfile[user_selected_tree_path]
        except KeyError as e:
            print("Error: Invalid key when searching for experiment configuration attributes.")
            print("Key Error: {0} {1}".format(e.errno, e.strerror))
            return
        # At this point dataset points to a valid HDF5 dataset containing data as an np.ndarray.
        # Construct dictionary of experiment settings from HDF5 dataset attributes
        data_settings = {}
        for key in dataset.attrs:
            if isinstance(dataset.attrs[key], (np.float64, np.float32, np.float16, float)):
                data_settings[key] = round(float(dataset.attrs[key]), 2)
            else:
                data_settings[key] = dataset.attrs[key]
        hfile.close()
        if isinstance(data, np.ndarray) and data.dtype is not object:
            print("Outputting HDF5 dataset and settings dict ...")
            self.outputData(data, data_settings)
        else:
            print("Error: Failed to create array from HDF5 dataset; possible incompatibale dtype.")
            return

    def outputData(self, data, data_settings=None):
        """Output valid np.ndarray to main GUI for visualization."""
        # print("Sending array from HDF5 to main UI.")
        # print("Array attributes: dtype={0}, shape={1}.".format(data.dtype, data.shape))
        self.output_array_signal.emit(data)
        self.output_array_attrs_signal.emit(data_settings)
        self.close()


class HDF5TreeModel(QtGui.QStandardItemModel):
    """Model for HDF5 tree heirarchy."""

    def __init__(self, hfile_path):
        """Init invisible root; hide headers.

        :parameter hfile: string path to HDF5 file
        """
        super().__init__()
        self.toplevel_node = self.invisibleRootItem()  # invisible node
        # self.experiments_node = QtGui.QStandardItem("Experiments")  # first visible root
        # self.toplevel_node.appendRow(self.experiments_node)

        # open HDF5 file as read only
        self.hfile_path = hfile_path
        self.hfile = h5py.File(hfile_path, "r")
        self.populateTreeFromDict()
        self.hfile.close()

    def validatePath(self, path):
        """Check if a given path is valid in the current HDF5 file structure."""
        hfile = h5py.File(self.hfile_path, "r")
        return path in hfile

    def populateTreeFromDict(self):
        """Get dict representation of HDF5 tree and populate TreeView."""
        dtree = recursiveHDF5ToDict(self.hfile)
        recursiveDictToTree(self.toplevel_node, dtree)


def recursiveDictToTree(root, d):
    """Populate tree from dict."""
    for key, item in d.items():
        node = QtGui.QStandardItem(key)
        root.appendRow(node)
        if isinstance(item, dict):
            recursiveDictToTree(node, d[key])


def recursiveHDF5ToDict(hfile, path="/"):
    """Recursively walk the HDF5 file structure and convert to dict."""
    dtree = {}
    for key, item in hfile[path].items():
        if isinstance(item, h5py._hl.dataset.Dataset):
            dtree[key] = item.value
        elif isinstance(item, h5py._hl.group.Group):
            dtree[key] = recursiveHDF5ToDict(hfile, path=path+str(key)+"/")
    return dtree


def arrayToHDF5(path, group_name, dataset_name, data, compression=None):
    """Create HDF5 dataset from 3D Numpy Array.

    :arguement path: string path to location of HDF5 file to create
    :arguement group_name: HDF5 Group to place data into
    :arguement dataset_name:
    :arguement data: 3D numpy array to store in HDF5 format
    """
    valid_filters = ["gzip", "lzf", "szip"]
    try:
        h5file = h5py.File(path, 'w')
    except OSError:
        # TODO: fill in proper errors
        pass
    print("HDF5 file located at {}".format(path))
    if group_name not in h5file:
        group = h5file.create_group(group_name)
    else:
        print("Error: HDF5 file {0} already contains Group {1}".format(path, group_name))
        return
    if dataset_name not in group.keys():
        if compression is None:
            group.create_dataset(dataset_name, data=data)
        elif compression in valid_filters:
            group.create_dataset(dataset_name,
                                 data=data,
                                 compression=compression)
        else:
            print("Error: Invalid Compression type provided when creating HDF5 dataset")
            print("Valid compression types are {}".format(valid_filters))
            return

    else:
        print("Error: HDF5 file {0} already contains dataset name {1} in Group {2}".format(path,
                                                                                           dataset_name,
                                                                                           group_name))
        return
    h5file.close()


def HDF5ToArray(hfile_path, hdf5_path_to_data=None):
    """Create 3D Numpy array from HDF5 file.

    :arguement path: string path to HDF5 file to open
    :return: None if query fails, else numpy array from HDF5 dataset.
    """
    if hdf5_path_to_data is None:
        print("Error: No data path provided to search HDF5 tree.")
        return None
    try:
        hfile = h5py.File(hfile_path, "r")
    except OSError:
        # TODO: fill in proper errors
        pass
    try:
        dataset = hfile[hdf5_path_to_data]
    except KeyError:
        print("Error: No data located at {0} in HDF5 file{1}.".format(hdf5_path_to_data, hfile_path))
        return None
    if isinstance(dataset, h5py._hl.group.Group):
        print("Error: path to data in HDF5 file selected a Group not a Dataset.")
        return None
    elif isinstance(dataset, h5py._hl.dataset.Dataset):
        return np.array(dataset)
    else:
        return None


def h_line():
    """Convienience to quickly add UI separators."""
    f = QtWidgets.QFrame()
    f.setFrameShape(QtWidgets.QFrame.HLine)
    f.setFrameShadow(QtWidgets.QFrame.Sunken)
    return f


def v_line():
    """Convienience to quickly add UI separators."""
    f = QtWidgets.QFrame()
    f.setFrameShape(QtWidgets.QFrame.VLine)
    f.setFrameShadow(QtWidgets.QFrame.Sunken)
    return f


def main():
    """Test."""
    app = QtWidgets.QApplication(sys.argv)
    data_model = HDF5TreeModel("./source/Experiments.h5")
    tv = HDF5Viewer(data_model)
    tv.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
