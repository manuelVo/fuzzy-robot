from PySide.QtCore import *
from PySide.QtGui import *
import os
import configuration as config


class GameList(QListView):
    def __init__(self, parent):
        super().__init__(parent)
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.init_ui()

    def init_ui(self):
        self.model.appendRow(QStandardItem("test"))
        pass

    def set_games(self, games, default_state=Qt.PartiallyChecked):
        self.model.clear()
        for game in games:
            item = QStandardItem()
            item.setText(game.name)
            item.setIcon(QIcon(os.path.join(config.game_images_folder, game.id + ".png")))
            item.setCheckable(True)
            item.setCheckState(default_state)
            item.game = game
            self.model.appendRow(item)
            self.show()

