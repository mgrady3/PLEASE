"""
PLEASE - The Python Low-energy Electron Analysis SuitE.

Author: Maxwell Grady
Affiliation: University of New Hampshire Department of Physics Pohl group
Version 1.0.0
Date: April, 2017

Entrypoint for PLEASE.

Usage:
    python /path/to/main.py

    This will load the application and instantiate the GUI.
"""
# Stdlib and Scientific Stack imports
import os
import sys
import traceback
import pyqtgraph as pg
from PyQt5 import QtWidgets

# Local Project imports
from please import MainWindow


__Version = '1.0.0'
# __imgorder = 'row-major'  # pyqtgraph global setting


def custom_exception_handler(exc_type, exc_value, exc_traceback):
    """Allow printing of unhandled exceptions instead of Qt Abort."""
    if issubclass(exc_type, KeyboardInterrupt):
        QtWidgets.QApplication.instance().quit()

    print("".join(traceback.format_exception(exc_type,
                                             exc_value,
                                             exc_traceback)))


def main():
    """Start Qt Event Loop and display main window."""
    # print("Welcome to PLEASE. Installing Custom Exception Handler ...")
    sys.excepthook = custom_exception_handler
    # print("Initializing Qt Event Loop ...")
    app = QtWidgets.QApplication(sys.argv)

    # pyqtgraph settings
    # pg.setConfigOption('imageAxisOrder', __imgorder)

    # print("Creating Please App ...")
    mw = MainWindow(v=__Version)
    mw.showMaximized()

    # This is a big fix for PyQt5 on macOS
    # When running a PyQt5 application that is not bundled into a
    # macOS app bundle; the main menu will not be clickable until you
    # switch to another application then switch back.
    # Thus to fix this we execute a quick applescript from the file
    # cmd.scpt which automates the keystroke "Cmd+Tab" twice to swap
    # applications then immediately swap back and set Focus to the main window.
    if "darwin" in sys.platform:
        import please
        sourcepath = os.path.dirname(please.__file__)
        cmdpath = os.path.join(sourcepath, 'cmd.scpt')
        cmd = """osascript {0}""".format(cmdpath)
        os.system(cmd)
        os.system(cmd)
        mw.viewer.setFocus()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
