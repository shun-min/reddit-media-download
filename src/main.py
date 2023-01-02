#!/usr/bin/python
import re
import sys

import m3u8_To_MP4
from PyQt5 import QtWidgets, QtCore

from utils import get_auth

class Downloader(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.video_links = list()
        self.init_ui()
        self.set_connections()

    def init_ui(self):
        self.setWindowTitle("m3u8 to mp4 Downloader")
        self.setFixedWidth(500)
        self.setFixedHeight(250)

        self.vlayout = QtWidgets.QVBoxLayout()
        self.src_layout = QtWidgets.QHBoxLayout()
        self.src_label = QtWidgets.QLabel("Paste url to scrape:")
        self.url_txt = QtWidgets.QLineEdit()
        self.path_label = QtWidgets.QLabel("Download to directory")
        self.dst_layout = QtWidgets.QHBoxLayout()
        self.dst_label = QtWidgets.QLabel("Select destination folder")
        self.dir_btn = QtWidgets.QPushButton("Select...")
        self.get_media_btn = QtWidgets.QPushButton("Get Media from URL")
        self.downlaod_path_txt = QtWidgets.QLineEdit()
        self.download_btn = QtWidgets.QPushButton("Download")

        self.video_tree_list = QtWidgets.QTreeWidget()
        self.img_tree_list = QtWidgets.QTreeWidget()

        self.media_layout = QtWidgets.QHBoxLayout()
        self.media_layout.addWidget(self.video_tree_list)
        self.media_layout.addWidget(self.img_tree_list)

        self.src_layout.addWidget(self.src_label)
        self.src_layout.addWidget(self.url_txt)
        self.src_layout.addWidget(self.get_media_btn)

        self.dst_layout.addWidget(self.downlaod_path_txt)
        self.dst_layout.addWidget(self.dir_btn)

        self.vlayout.addLayout(self.src_layout)
        self.vlayout.addLayout(self.media_layout)
        self.vlayout.insertSpacing(1, 20)
        self.vlayout.addWidget(self.dst_label)
        self.vlayout.addLayout(self.dst_layout)
        self.vlayout.addWidget(self.download_btn)

        self.setLayout(self.vlayout)

    def set_connections(self):
        self.dir_btn.clicked.connect(self.set_directory)
        self.get_media_btn.clicked.connect(self.get_media_links)
        self.download_btn.clicked.connect(self.download)


    def add_media_to_tree(self):
        for media_item in self.video_links:
            tree_item = QtWidgets.QTreeWidgetItem(self.video_tree_list)
            tree_item.setText(0, media_item)

    def get_media_links(self):
        data = get_auth(self.url_txt.text())
        parent_lists = list()
        for d in data:
            children = d["data"]["children"]
            for c in children:
                try:
                    parent_list = c["data"]["crosspost_parent_list"]
                    parent_lists.append(parent_list)
                except KeyError:
                    continue

        for p in parent_lists:
            try:
                video_link = p[0]["media"]["reddit_video"]["fallback_url"]
                self.video_links.append(video_link)
            except KeyError:
                continue

        self.add_media_to_tree()

    def set_directory(self):
        folder_path = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select..."))
        self.downlaod_path_txt.setText(folder_path)

    def download(self):
        m3u8_To_MP4.download(self.url_txt.text(), mp4_file_dir=self.url)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    downlaoder = Downloader()
    downlaoder.show()

    sys.exit(app.exec_())