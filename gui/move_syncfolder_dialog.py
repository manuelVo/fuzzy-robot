from PySide.QtGui import *
from enum import Enum

class MoveSyncfolderDialog(QDialog):

    def __init__(self):
        super(MoveSyncfolderDialog, self).__init__()
        self.move = True

        self.setWindowTitle("Chnage sync folder")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        label = QLabel("Savegames exist in the old sync folder. What do you want to do with them?", self)
        layout.addWidget(label)

        button_move = QPushButton("Move them to the new sync folder", self)
        button_move.clicked.connect(lambda: self.accept(True))
        layout.addWidget(button_move)

        button_leave = QPushButton("Leave them where they are", self)
        button_leave.clicked.connect(lambda: self.accept(False))
        layout.addWidget(button_leave)

    def accept(self, move):
        self.move = move
        super(MoveSyncfolderDialog, self).accept()
