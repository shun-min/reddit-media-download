#!/usr/bin/python
import sys
import m3u8_To_MP4
from PySide2 import QtWidgets, QtGui, QtCore


class Downloader(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.dialog = QtWidgets.QDialog()
        self.layout = QtWidgets.QHBoxLayout()
        self.path_txt = QtWidgets.QLineEdit()
        self.download_btn = QtWidgets.QPushButton("Download")

        self.layout.addWidget(self.path_txt)
        self.layout.addWidget(self.download_btn)

        self.setLayout(self.layout)

    def set_connections(self):
        self.download_btn.clicked.connect(self.download)

    def download(self):
        m3u8_To_MP4.download("https://v.redd.it/gi4n5i6qeyt81/HLSPlaylist.m3u8")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    downlaoder = Downloader()
    downlaoder.show()

    sys.exit(app.exec_())