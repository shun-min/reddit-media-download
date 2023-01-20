#!/usr/bin/python
import os
import sys
import urllib

from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from utils import get_auth, get_url_response


class Downloader(QDialog):
    def __init__(self):
        super().__init__()
        self.download_dest = None
        self.video_links = list()
        self.image_links = list()
        self.selected_media = list()
        self.init_ui()
        self.set_connections()

    def init_ui(self):
        self.setWindowTitle("Media Downloader")
        self.setMinimumWidth(500)
        self.setMinimumHeight(250)

        self.vlayout = QVBoxLayout()
        self.src_layout = QHBoxLayout()
        self.src_label = QLabel("Paste url to scrape:")
        self.url_txt = QLineEdit()
        self.path_label = QLabel("Download to directory")
        self.dst_layout = QHBoxLayout()
        self.dst_label = QLabel("Select destination folder")
        self.dir_btn = QPushButton("Select...")
        self.get_media_btn = QPushButton("Get Media from URL")
        self.download_path_lineedit = QLineEdit()
        # TODO: remove
        # https://www.reddit.com/r/test_random/comments/10guglg/testing_imgs
        # https://reddit.com/r/malaysia/comments/vcnhkc/daylight_supermoon_near_the_tip_of_kl_twin_towers
        # https://www.reddit.com/r/cinematography/comments/10gfw97/how_would_you_achieve_this_sort_of_shot_wide
        self.url_txt.setText("https://www.reddit.com/r/cinematography/comments/10gfw97/how_would_you_achieve_this_sort_of_shot_wide")
        self.download_btn = QPushButton("Download")

        self.video_label = QLabel("Videos: ")
        self.video_tree_list = QTreeView()
        self.video_tree_list.setHeaderHidden(True)
        self.image_label = QLabel("Images: ")
        self.img_tree_list = QTreeView()
        self.img_tree_list.setHeaderHidden(True)

        self.media_layout = QHBoxLayout()
        self.video_layout = QVBoxLayout()
        self.image_layout = QVBoxLayout()
        self.video_layout.addWidget(self.video_label)
        self.video_layout.addWidget(self.video_tree_list)
        self.image_layout.addWidget(self.image_label)
        self.image_layout.addWidget(self.img_tree_list)
        self.media_layout.addLayout(self.video_layout)
        self.media_layout.addLayout(self.image_layout)

        self.src_layout.addWidget(self.src_label)
        self.src_layout.addWidget(self.url_txt)
        self.src_layout.addWidget(self.get_media_btn)

        self.dst_layout.addWidget(self.download_path_lineedit)
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
        if self.video_links:
            tree_item = QStringListModel()
            tree_item.setStringList(self.video_links)
            self.video_tree_list.setModel(tree_item)
            # TODO: add feature to multi-select media to download
            self.selected_media.extend(self.video_links)

        if self.image_links:
            img_tree_item = QStringListModel()
            img_tree_item.setStringList(self.image_links)
            self.img_tree_list.setModel(img_tree_item)
            self.selected_media.extend(self.image_links)

    def get_media_links(self):
        # https://reddit.com/r/malaysia/comments/vcnhkc/daylight_supermoon_near_the_tip_of_kl_twin_towers
        # https://v.redd.it/cjurndouho591/DASH_1080.mp4?source=fallback
        header = get_auth()
        data = get_url_response(header, self.url_txt.text())
        video_parent_list = list()
        for d in data:
            children = d["data"]["children"]
            for c in children:
                # TODO: handle img galleries
                try:
                    img_item = c["data"]["url"]
                    self.image_links.append(img_item)
                except KeyError:
                    continue
            for c in children:
                try:
                    parent_list = c["data"]["crosspost_parent_list"]
                    video_parent_list.append(parent_list)
                except KeyError:
                    continue

        for p in video_parent_list:
            try:
                video_link = p[0]["media"]["reddit_video"]["fallback_url"]
                self.media_links.append(video_link)
            except KeyError:
                continue

        self.add_media_to_tree()

    def set_directory(self):
        folder_path = str(QFileDialog.getExistingDirectory(self, "Select..."))
        self.download_path_lineedit.setText(folder_path)
        self.download_dest = self.download_path_lineedit.text()

    def download(self):
        for media in self.selected_media:
            if ".mp4" in media:
                ext = ".mp4"
            else:
                ext = ".jpg"
            dst_file = os.path.join(self.download_dest, str(self.selected_media.index(media)) + ext)
            dest_path = Path(dst_file)
            with urllib.request.urlopen(media) as response, open(dest_path, 'wb') as x:
                data = response.read()
                x.write(data)


if __name__ == "__main__":
    app = QApplication([])

    downlaoder = Downloader()
    downlaoder.show()

    sys.exit(app.exec_())
