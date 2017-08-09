"""Test functionality for QTreeView widgets.

This file contains:
Simple test class with TreeView built by hand

More complex set of classes for building a QTreeView
from an HDF5 tree heirarchy.
"""

import h5py
import sys
from PyQt5 import QtGui, QtWidgets


class TestTreeView(QtWidgets.QMainWindow):
    """Toplevel window to contain a TreeView."""

    def __init__(self, parent=None):
        """Init MainWindow and set Central widget."""
        super().__init__(parent)
        self.treeview = QtWidgets.QTreeView()
        self.setCentralWidget(self.treeview)
        self.createModel()
        self.createItems()
        self.populateTree()
        self.treeview.setModel(self.item_model)
        self.treeview.header().hide()

    def createModel(self):
        """Setup StandardItemModel."""
        self.item_model = QtGui.QStandardItemModel()
        self.top_node = self.item_model.invisibleRootItem()

    def createItems(self):
        """Create Nodes to populate self.treeview."""
        self.root_node = QtGui.QStandardItem("Experiments")
        experiment_types = ["LEED", "LEEM", "PEEM"]
        self.experiment_type_nodes = [QtGui.QStandardItem(name) for name in experiment_types]

        LEED_experiment_materials = ["MoS2", "BP", "SnSe2", "Graphene"]
        self.LEED_experiment_nodes = [QtGui.QStandardItem(material) for material in LEED_experiment_materials]

        LEEM_experiment_materials = ["MoS2", "Graphene", "Ru"]
        self.LEEM_experiment_nodes = [QtGui.QStandardItem(material) for material in LEEM_experiment_materials]

        PEEM_experiment_materials = ["Graphene", "Ru"]
        self.PEEM_experiment_nodes = [QtGui.QStandardItem(material) for material in PEEM_experiment_materials]

    def populateTree(self):
        """Add Nodes to model."""
        self.top_node.appendRow(self.root_node)
        for node in self.experiment_type_nodes:
            self.root_node.appendRow(node)
        for node in self.LEED_experiment_nodes:
            self.experiment_type_nodes[0].appendRow(node)
        for node in self.LEEM_experiment_nodes:
            self.experiment_type_nodes[1].appendRow(node)
        for node in self.PEEM_experiment_nodes:
            self.experiment_type_nodes[2].appendRow(node)


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


def main():
    """Start app and display treeview."""
    app = QtWidgets.QApplication(sys.argv)

    # Uncomment this section for simple test
    # tv = TestTreeView()
    # tv.show()

    # This section tests building a TreeView from HDF5 tree
    data = HDF5TreeModel("Testv1.h5")
    tv = HDF5Viewer(data)
    tv.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
