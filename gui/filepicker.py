from PySide2.QtWidgets import *
import os.path
import platform
import configuration as config


class Filepicker(QWidget):
    def __init__(self, filedialog=None, parent=None):
        super(Filepicker, self).__init__(parent)

        self.filedialog = filedialog

        layout = QHBoxLayout(self)

        self.textbox = QLineEdit(self)
        layout.addWidget(self.textbox)

        browse_button = QPushButton("Browse…", self)
        browse_button.clicked.connect(self.browse)
        layout.addWidget(browse_button)

    def set_filedialog(self, filedialog):
        self.filedialog = filedialog

    def set_file(self, file):
        self.textbox.setText(file)

    def get_file(self):
        return self.textbox.text()

    def browse(self):
        if self.filedialog is not None:
            file = self.textbox.text()
            if os.path.exists(file):
                self.filedialog.setDirectory(file)
            else:
                if platform.system() == "Windows":
                    file = "%USERPROFILE%"
                else:
                    file = "~"
                self.filedialog.setDirectory(config.expand_path(file))
            if self.filedialog.exec():
                self.textbox.setText(self.filedialog.selectedFiles()[0])
