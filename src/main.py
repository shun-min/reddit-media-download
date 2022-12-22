#!/usr/bin/python
import re
import sys
from urllib.request import Request, urlopen

import m3u8_To_MP4
from PyQt5 import QtWidgets


class Downloader(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
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
        self.downlaod_path_txt = QtWidgets.QLineEdit()
        self.download_btn = QtWidgets.QPushButton("Download")

        self.src_layout.addWidget(self.src_label)
        self.src_layout.addWidget(self.url_txt)

        self.dst_layout.addWidget(self.downlaod_path_txt)
        self.dst_layout.addWidget(self.dir_btn)

        self.vlayout.addLayout(self.src_layout)
        self.vlayout.insertSpacing(1, 20)
        self.vlayout.addWidget(self.dst_label)
        self.vlayout.addLayout(self.dst_layout)
        self.vlayout.addWidget(self.download_btn)

        self.setLayout(self.vlayout)

    def set_connections(self):
        self.dir_btn.clicked.connect(self.set_directory)
        self.download_btn.clicked.connect(self.download)

    def set_directory(self):
        folder_path = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select..."))
        self.downlaod_path_txt.setText(folder_path)

    def download(self):
        url = self.scrape_for_url(self.downlaod_path_txt.text())
        m3u8_To_MP4.download(self.url_txt.text(), mp4_file_dir=url)

    def scrape_for_url(self, url):
        # url = "https://www.reddit.com/r/malaysia/comments/vcnhkc/daylight_supermoon_near_the_tip_of_kl_twin_towers/"
        user_agent = {'User-agent': 'Mozilla/5.0'}
        req = Request(url, headers=user_agent)
        page = urlopen(req)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        # TODO: Test string for UI dev
        # html = '123https://v.redd.it/0sljhvn5sm5a1/HLSPlaylist.m3u8123'
        ext = "m3u8"
        raw_pattern = r".+(?P<link>https.+.{}).+".format(ext)
        pattern = re.compile(raw_pattern)
        results = re.findall(pattern, html)
        return results


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    downlaoder = Downloader()
    downlaoder.show()

    sys.exit(app.exec_())