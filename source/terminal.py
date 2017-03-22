"""PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: February, 2017

Contained here are all classes for creating a mock Terminal widget
which can be docked to the QMainWindow and receive messages from stdout/stderr
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class CustomStream(QtCore.QObject):
    """Send messages to arbitrary widget."""

    message = QtCore.pyqtSignal(str)

    def __init__(self):
        """Just initialize super class, no instance variables needed."""
        super(QtCore.QObject, self).__init__()

    def write(self, message):
        """Assume message can be cast to string."""
        self.message.emit(str(message))

    def flush(self):
        """Overloaded for stream interface."""
        pass


class MessageConsole(QtWidgets.QWidget):
    """TextArea to collect messages rerouted from sys.stdout.

    Will be contained in a DockWidget dockable to the bottom
    of the QMainWindow.
    """

    def __init__(self):
        """Initialize TextEdit and CustomStream.

        Reroute sys.stdout and sys.stderr to print to QTextEdit
        Disable user edits on QTextEdit (ReadOnly)
        """
        super(QtWidgets.QWidget, self).__init__()

        layout = QtWidgets.QVBoxLayout()
        self.textedit = QtWidgets.QTextEdit()
        self.textedit.setReadOnly(True)
        layout.addWidget(self.textedit)
        self.setLayout(layout)

        self.stream = CustomStream()
        self.stream.message.connect(self.set_message)

        sys.stdout = self.stream
        sys.stderr = self.stream
        self.welcome()
        self.show()

    @QtCore.pyqtSlot(str)
    def set_message(self, message):
        """Update QTextEdit with string from sys.stdout or sys.stderr."""
        self.textedit.moveCursor(QtGui.QTextCursor.End)
        self.textedit.insertPlainText(message)

    def closeEvent(self, event):
        """Override closeEvent to reset sys.stdout and sys.stderr."""
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        super(MessageConsole, self).closeEvent(event)

    @staticmethod
    def welcome():
        """Called on instantiation of MessageConsole."""
        print("Welcome to PLEASE!")
        print("Use the button bar to the left to load data for analysis.")
