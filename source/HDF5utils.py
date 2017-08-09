"""
PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: April, 2017

HDF5utils.py

Collection of utility methods and classes for working with HDF5 data
"""

import h5py
import numpy as np
from PyQt import QtGui, QtWidgets


class HDF5Viewer(QtWidgets.QWidget):
    """Container for QTreeView populated from HDF5."""

    def __init__(self, model, parent=None):
        """Init view and set model."""
        super().__init__(parent)
        self.treeview = QtWidgets.QTreeView()
        self.model = model
        self.treeview.setModel(model)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.treeview)
        self.setLayout(self.layout)


class HDF5TreeModel(QtGui.QStandardItemModel):
    """Model for HDF5 tree heirarchy."""

    def __init__(self, hfile):
        """Init invisible root; hide headers.

        :parameter hfile: string path to HDF5 file
        """
        super().__init__()
        self.toplevel_node = self.invisibleRootItem()  # invisible node
        self.experiments_node = QtGui.QStandardItem("Experiments")  # first visible root
        self.toplevel_node.appendRow(self.experiments_node)
        # open HDF5 file as read only
        self.hfile = h5py.File(hfile, "r")
        self.populateTreeFromDict()
        self.hfile.close()

    def populateTreeFromDict(self):
        """Get dict representation of HDF5 tree and populate TreeView."""
        dtree = recursiveHDF5ToDict(self.hfile)
        recursiveDictToTree(self.experiments_node, dtree)


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


def HDF5ToArray(path, group_name="/", dataset_name=None):
    """Create 3D Numpy array from HDF5 file.
    :arguement path: string path to HDF5 file to open
    :arguement group_name: string indicating which group within the HDF5 DB to search for data
    :arguement dataset_name: string indicating which dataset to load from group_name
    :return: None if query fails, else numpy array from HDF5 dataset.
    """

    try:
        hfile = h5py.File(path, "r")
    except OSError:
        # TODO: fill in proper errors
        pass
    try:
        dataset = hfile[group_name + "/" + dataset_name]
    except KeyError:
        print("Error: No dataset named {0} in HDF5 file {1} in Group name {2}.".format(dataset_name, path, group_name))
        return None
    return np.array(dataset)
