from PySide.QtCore import *
from PySide.QtGui import *
from gui.game_list import GameList
import savesync
import configuration as config


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.list_found_games = None
        self.list_synchronized_games = None
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

        config.load()
        games = savesync.detect_games()
        self.list_found_games.set_games([game for game in games if not game.is_synchronized], Qt.Checked)
        self.list_synchronized_games.set_games([game for game in games if game.is_synchronized], Qt.Unchecked)

        self.center()

    def center(self):
        geometry = self.frameGeometry()
        geometry.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(geometry.topLeft())
        self.show()

    def synchronize_games(self):
        model = self.list_found_games.model
        for row in range(0, model.rowCount()):
            item = model.item(row)
            if item.checkState() == Qt.Checked:
                # TODO Check for conflicts
                savesync.move_save_to_cloud(item.game)
        games = savesync.detect_games()
        self.list_found_games.set_games([game for game in games if not game.is_synchronized], Qt.Checked)
        self.list_synchronized_games.set_games([game for game in games if game.is_synchronized], Qt.Unchecked)

    def update_games_list(self):
        config.update_games()
        games = savesync.detect_games()
        self.list_found_games.set_games([game for game in games if not game.is_synchronized], Qt.Checked)
        self.list_synchronized_games.set_games([game for game in games if game.is_synchronized], Qt.Unchecked)
        pass