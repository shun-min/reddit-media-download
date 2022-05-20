#!/usr/bin/python
import sys
import m3u8_To_MP4
from PySide2 import QtWidgets, QtGui, QtCore


class Downloader(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.label = QtWidgets.QLabel("Paste path to download")
        self.layout = QtWidgets.QHBoxLayout()
        self.link_txt = QtWidgets.QLineEdit()
        self.downlaod_path_txt = QtWidgets.QLineEdit()
        self.download_btn = QtWidgets.QPushButton("Download")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.link_txt)
        self.layout.addWidget(self.downlaod_path_txt)
        self.layout.addWidget(self.download_btn)

        self.setLayout(self.layout)

    def set_connections(self):
        self.download_btn.clicked.connect(self.download)

    def download(self):
        # https://v.redd.it/gi4n5i6qeyt81/HLSPlaylist.m3u8
        #/home/lam/Documents/PycharmProjects/m3u8Download/sample
        m3u8_To_MP4.download(self.link_txt.text(), mp4_file_dir=self.downlaod_path_txt.text())

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    downlaoder = Downloader()
    downlaoder.show()

    sys.exit(app.exec_())