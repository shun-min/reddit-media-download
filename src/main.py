#!/usr/bin/python
import re
import sys
import requests
import requests.auth

from utils import REDDIT

import m3u8_To_MP4
from PyQt5 import QtWidgets, QtCore

id = REDDIT.ID
secret = REDDIT.SECRET
username = REDDIT.USERNAME
password = REDDIT.PASSWORD


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
        self.get_media_btn = QtWidgets.QPushButton("Get Media from URL")
        self.downlaod_path_txt = QtWidgets.QLineEdit()
        self.download_btn = QtWidgets.QPushButton("Download")

        self.media_tree_list = QtWidgets.QTreeWidget()

        self.src_layout.addWidget(self.src_label)
        self.src_layout.addWidget(self.url_txt)
        self.src_layout.addWidget(self.get_media_btn)

        self.dst_layout.addWidget(self.downlaod_path_txt)
        self.dst_layout.addWidget(self.dir_btn)

        self.vlayout.addLayout(self.src_layout)
        self.vlayout.addWidget(self.media_tree_list)
        self.vlayout.insertSpacing(1, 20)
        self.vlayout.addWidget(self.dst_label)
        self.vlayout.addLayout(self.dst_layout)
        self.vlayout.addWidget(self.download_btn)

        self.setLayout(self.vlayout)

        # self.get_media_signal = QtCore.pyqtSignal()
        # self.get_media_signal.connect(self.get_media_btn)

    def set_connections(self):
        self.dir_btn.clicked.connect(self.set_directory)
        self.get_media_btn.clicked.connect(self.get_media_links)
        self.download_btn.clicked.connect(self.download)

    def get_auth(self):
        # getting reddit authentication info
        client_auth = requests.auth.HTTPBasicAuth(id, secret)
        post_data = {"grant_type": "password", "username": username, "password": password}
        headers = {
            "User-Agent": "Reddit automation script"
        }

        # get token access ID
        TOKEN_ACCESS_ENDPOINT = "https://www.reddit.com/api/v1/access_token"
        response = requests.post(TOKEN_ACCESS_ENDPOINT, data=post_data, headers=headers, auth=client_auth)
        if response.status_code == 200:
            token_id = response.json()["access_token"]

        # use API to get json object of a subreddit page
        OAUTH_ENDPOINT = "https://oauth.reddit.com"
        params = {
            "limit": 100
        }
        header2 = {
            "User-Agent": "Reddit automation script",
            "Authorization": "Bearer" + token_id
        }
        # https://reddit.com/r/malaysia/comments/vcnhkc/daylight_supermoon_near_the_tip_of_kl_twin_towers/.json
        subreddit_url = self.url_txt.text().split("reddit.com")[1] + ".json"
        response2 = requests.get(OAUTH_ENDPOINT + subreddit_url, headers=header2, params=params)
        if response2.status_code == 200:
            data = response2.json()
        return data

    def add_media_to_tree(self):
        for media_item in self.video_links:
            tree_item = QtWidgets.QTreeWidgetItem(self.media_tree_list)
            tree_item.setText(0, media_item)
    def get_media_links(self):
        data = self.get_auth()
        parent_lists = list()
        for d in data:
            children = d["data"]["children"]
            for c in children:
                try:
                    parent_list = c["data"]["crosspost_parent_list"]
                    parent_lists.append(parent_list)
                except KeyError:
                    continue

        self.video_links = list()
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
        url = self.scrape_for_url(self.downlaod_path_txt.text())
        m3u8_To_MP4.download(self.url_txt.text(), mp4_file_dir=url)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    downlaoder = Downloader()
    downlaoder.show()

    sys.exit(app.exec_())