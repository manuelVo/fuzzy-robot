import sys
from PySide.QtGui import *
from gui.main_window import MainWindow

app = QApplication(sys.argv)
main_window = MainWindow()

sys.exit(app.exec_())
