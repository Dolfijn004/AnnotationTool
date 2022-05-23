#converting ui file to python using pyqt6
#pyuic6 -x demo.ui -o demo.py
#-----------------
#converting ui file to python using pyside6
#pyside6-uic filename.ui > filename.py

import sys
from PySide6 import QtWidgets
from demo import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

    #here create your functions



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()