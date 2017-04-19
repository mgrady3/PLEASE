"""Test Splash Screen with Progress Bar."""

import os
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets


def main():
    app = QtWidgets.QApplication(sys.argv)
    thispath = __file__
    rootpath = os.path.join(os.path.dirname(thispath), os.pardir)
    imagedir = os.path.join(rootpath, "Images")
    splashimagepath = os.path.join(imagedir, "Splash.png")
    splashimage = QtGui.QPixmap(splashimagepath)
    splashscreen = QtWidgets.QSplashScreen(splashimage, QtCore.Qt.WindowStaysOnTopHint)
    splashscreen.setMask(splashimage.mask())

    progressbar = QtWidgets.QProgressBar(splashscreen)
    progressbar.setGeometry(splashscreen.width()/10, 9*splashscreen.height()/10,
                            8*splashscreen.width()/10, splashscreen.height()/10)

    splashscreen.show()

    mw = QtWidgets.QMainWindow()
    mw.setWindowTitle("Test")
    app.processEvents()

    p = 0
    while p <= 100:
        app.processEvents()
        progressbar.setValue(p)
        app.processEvents()
        time.sleep(1)
        app.processEvents()
        p += 20

    mw.show()
    splashscreen.finish(mw)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
