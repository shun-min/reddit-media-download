#!/usr/bin/python
import os
import sys

import m3u8_To_MP4
from PySide2 import QtWidgets, QtGui, QtCore


class Downloader(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.set_connections()

    def init_ui(self):
        self.vlayout = QtWidgets.QVBoxLayout()
        self.instr_label = QtWidgets.QLabel("Paste url to download")
        self.link_txt = QtWidgets.QLineEdit()
        self.path_label = QtWidgets.QLabel("Download to directory")

        self.hlayout = QtWidgets.QHBoxLayout()
        self.dir_btn = QtWidgets.QPushButton("Select...")
        self.downlaod_path_txt = QtWidgets.QLineEdit()
        self.download_btn = QtWidgets.QPushButton("Download")

        self.hlayout.addWidget(self.downlaod_path_txt)
        self.hlayout.addWidget(self.dir_btn)

        self.vlayout.addWidget(self.instr_label)
        self.vlayout.addWidget(self.link_txt)
        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addWidget(self.download_btn)

        self.setLayout(self.vlayout)

    def set_connections(self):
        self.dir_btn.clicked.connect(self.open_explorer)
        self.download_btn.clicked.connect(self.download)

    def open_explorer(self):
        os.system("xdg-open '%s'" % "/home")

    def download(self):
        # https://v.redd.it/gi4n5i6qeyt81/HLSPlaylist.m3u8wecha
        #/home/lam/Documents/PycharmProjects/m3u8Download/sample
        print("<<<<<<{} {}".format(self.link_txt.text(), self.downlaod_path_txt.text()))
        m3u8_To_MP4.download(self.link_txt.text(), mp4_file_dir=self.downlaod_path_txt.text())

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    downlaoder = Downloader()
    downlaoder.show()

    sys.exit(app.exec_())