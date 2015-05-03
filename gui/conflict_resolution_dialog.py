from PySide.QtGui import *
from PySide.QtCore import *
from enum import Enum


class ConflictResolutionDialog(QDialog):
    def __init__(self, game_name):
        super(ConflictResolutionDialog, self).__init__()

        self.method = ConflictResolutionDialog.ResolutionMethod.DONT_SYNC
        self.checkbox_remind = QCheckBox(self)

        # Remove the close button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        self.setWindowTitle("Conflict")
        self.init_ui(game_name)

    def init_ui(self, game_name):
        layout = QVBoxLayout(self)

        label = QLabel("The are synchronized and local savegames for '" + game_name + "'. What do you want to do.")
        layout.addWidget(label)

        button_overwrite_local = QPushButton("Overwrite local savegame", self)
        button_overwrite_local.clicked.connect(lambda: self.accept(ConflictResolutionDialog.ResolutionMethod.OVERWRITE_LOCAL))
        layout.addWidget(button_overwrite_local)

        button_overwrite_cloud = QPushButton("Overwrite cloud savegame", self)
        button_overwrite_cloud.clicked.connect(lambda: self.accept(ConflictResolutionDialog.ResolutionMethod.OVERWRITE_CLOUD))
        layout.addWidget(button_overwrite_cloud)

        button_overwrite_local = QPushButton("Don't sync game", self)
        button_overwrite_local.clicked.connect(lambda: self.accept(ConflictResolutionDialog.ResolutionMethod.DONT_SYNC))
        layout.addWidget(button_overwrite_local)

        self.checkbox_remind.setText("Remember for future conflicts")
        self.checkbox_remind.setTristate(False)
        self.checkbox_remind.setCheckState(Qt.Unchecked)
        layout.addWidget(self.checkbox_remind)

    def accept(self, method):
        self.method = method
        super(ConflictResolutionDialog, self).accept()

    def get_dialog_result(self):
        return self.method, True if self.checkbox_remind.checkState() == Qt.Checked else False

    class ResolutionMethod(Enum):
        OVERWRITE_LOCAL = 0,
        OVERWRITE_CLOUD = 1,
        DONT_SYNC = 2