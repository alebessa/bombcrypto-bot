from PyQt6 import QtCore, QtWidgets
from shared import resource_path
QtCore.QDir.addSearchPath('images', resource_path('gui/images/'))

import sys

from gui.main_window import Ui_MainWindow

def frontend(engine):
    
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()

    ui = Ui_MainWindow(engine)
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec())