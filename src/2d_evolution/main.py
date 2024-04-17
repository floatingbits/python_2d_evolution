from PyQt5.QtWidgets import QApplication

import sys
from widgets import MainWindow


app = QApplication(sys.argv)
w = MainWindow()
app.exec()
