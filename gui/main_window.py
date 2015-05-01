from PySide.QtCore import *
from PySide.QtGui import *
from gui.game_list import GameList
from gui.syncfolder_picker import SyncfolderPicker
import savesync
import configuration as config


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.list_found_games = None
        self.list_synchronized_games = None

        self.setWindowTitle("Fuzzy Robot")
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        label_found_games = QLabel("Found games", self)
        layout.addWidget(label_found_games, 0, 0)

        label_synchronized_games = QLabel("Synchronized games", self)
        layout.addWidget(label_synchronized_games, 0, 1)

        self.list_found_games = GameList(self)
        layout.addWidget(self.list_found_games, 1, 0)

        self.list_synchronized_games = GameList(self)
        layout.addWidget(self.list_synchronized_games, 1, 1)

        button_synchronize = QPushButton("Synchronize selected", self)
        button_synchronize.clicked.connect(self.synchronize_games)
        layout.addWidget(button_synchronize, 2, 0)

        button_group = QWidget(self)
        button_group_layout = QVBoxLayout(button_group)

        button_update = QPushButton("Update supported games list", self)
        button_update.clicked.connect(self.update_games_list)
        button_group_layout.addWidget(button_update)

        layout.addWidget(button_group, 1, 3, Qt.AlignTop)

        if not config.exists():
            folderpicker = SyncfolderPicker()
            if folderpicker.exec():
                config.cloudfolder = folderpicker.get_syncfolder()
                config.save()

        if config.exists():
            config.load()
            self.refresh_games()

        self.center()
        self.show()

    def center(self):
        geometry = self.frameGeometry()
        geometry.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(geometry.topLeft())

    def refresh_games(self):
        games = savesync.detect_games()
        self.list_found_games.set_games([game for game in games if not game.is_synchronized], Qt.Checked)
        self.list_synchronized_games.set_games([game for game in games if game.is_synchronized], Qt.Unchecked)

    def synchronize_games(self):
        if config.cloudfolder is None:
            folderpicker = SyncfolderPicker()
            if not folderpicker.exec():
                return
            config.cloudfolder = folderpicker.get_syncfolder()
            config.save()
            config.load()

        model = self.list_found_games.model
        for row in range(0, model.rowCount()):
            item = model.item(row)
            if item.checkState() == Qt.Checked:
                # TODO Check for conflicts
                savesync.move_save_to_cloud(item.game)
        self.refresh_games()

    def update_games_list(self):
        config.update_games()
        self.refresh_games()
