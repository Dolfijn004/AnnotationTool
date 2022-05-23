#converting ui file to python using pyqt6
#pyuic6 -x demo.ui -o demo.py
#-----------------
#converting ui file to python using pyside6
#pyside6-uic filename.ui > filename.py

import sys
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import *

from demo import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        #connect buttons with functions
        self.openButton.clicked.connect(self.displayMethod)

    #create your functions
    def displayMethod(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", QtCore.QDir.currentPath())
        if fileName:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer",
                                              "Cannot load %s." % fileName)
                return

            self.displayImage.setPixmap(QtGui.QPixmap.fromImage(image))
            self.displayImage.resize(image.width(), image.height())
            self.scaleFactor = 50


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()