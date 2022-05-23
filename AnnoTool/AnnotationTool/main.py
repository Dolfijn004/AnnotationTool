#converting ui file to python using pyqt6
#pyuic6 -x demo.ui -o demo.py
#-----------------
#converting ui file to python using pyside6
#pyside6-uic filename.ui > filename.py

import sys
from demo import Ui_MainWindow
from PySide6 import *
from PySide6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __int__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())