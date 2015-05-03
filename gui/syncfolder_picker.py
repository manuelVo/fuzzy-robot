from PySide.QtGui import *
import os.path
from gui.filepicker import Filepicker
import configuration as config


class SyncfolderPicker(QDialog):

    def __init__(self):
        super(SyncfolderPicker, self).__init__()
        self.filepicker = None
        self.syncfolder = None

        self.setWindowTitle("Select sync folder...")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        label = QLabel("Please select the folder to which you want your save synchronized", self)
        layout.addWidget(label)

        filedialog = QFileDialog()
        filedialog.setFileMode(filedialog.DirectoryOnly)
        self.filepicker = Filepicker(filedialog, self)
        self.filepicker.set_file(config.cloudfolder)
        layout.addWidget(self.filepicker)

        button_group = QWidget(self)
        button_group_layout = QHBoxLayout(button_group)

        button_cancel = QPushButton("Cancel", self)
        button_cancel.clicked.connect(self.reject)
        button_group_layout.addWidget(button_cancel)

        button_ok = QPushButton("Ok", self)
        button_ok.clicked.connect(self.buttonevent_accept)
        button_group_layout.addWidget(button_ok)

        layout.addWidget(button_group)

    def get_syncfolder(self):
        return self.filepicker.get_file()

    def buttonevent_accept(self):
        file = self.filepicker.get_file()
        if not os.path.exists(file):
            messagebox = QMessageBox()
            messagebox.setText("The specified folder does not exist")
            messagebox.setIcon(messagebox.Critical)
            messagebox.exec()
            return
        if not os.path.isdir(file):
            messagebox = QMessageBox()
            messagebox.setText("The specified path is not a folder")
            messagebox.setIcon(messagebox.Critical)
            messagebox.exec()
            return
        self.accept()