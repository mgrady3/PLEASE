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
import time
import traceback
from PyQt5 import QtCore, QtGui, QtWidgets

# Local Project imports
from please import MainWindow


__Version = '1.0.0'


def custom_exception_handler(exc_type, exc_value, exc_traceback):
    """Allow printing of unhandled exceptions instead of Qt Abort."""
    if issubclass(exc_type, KeyboardInterrupt):
        QtWidgets.QApplication.instance().quit()

    print("".join(traceback.format_exception(exc_type,
                                             exc_value,
                                             exc_traceback)))


def main():
    """Start Qt Event Loop and display main window."""
    sys.excepthook = custom_exception_handler

    app = QtWidgets.QApplication(sys.argv)

    # Setup QSplashScreen
    thispath = __file__
    rootpath = os.path.join(os.path.dirname(thispath), os.pardir)
    imagedir = os.path.join(rootpath, "Images")
    splashimagepath = os.path.join(imagedir, "Splash-scaled.png")
    splashimage = QtGui.QPixmap(splashimagepath)
    splashscreen = QtWidgets.QSplashScreen(splashimage, QtCore.Qt.WindowStaysOnTopHint)
    splashscreen.setMask(splashimage.mask())

    progressbar = QtWidgets.QProgressBar(splashscreen)
    xo = 32
    yo = 460
    w = 462
    h = 25
    # progressbar.setGeometry(splashscreen.width()/10, int(9.5*splashscreen.height()/10),
    #                        8*splashscreen.width()/10, splashscreen.height()/20)
    progressbar.setGeometry(xo, yo, w, h)

    splashscreen.show()
    app.processEvents()

    p = 0
    while p <= 100:
        app.processEvents()
        progressbar.setValue(p)
        app.processEvents()
        time.sleep(1)
        app.processEvents()
        p += 20

    mw = MainWindow(v=__Version)
    mw.showMaximized()
    splashscreen.finish(mw)

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
        # os.system(cmd)
        mw.viewer.setFocus()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
