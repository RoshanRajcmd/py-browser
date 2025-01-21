from PyQt5.QtWidgets import QPushButton, QToolBar
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon

class BookmarkBar(QToolBar):
    def __init__(self, mainWindow, title, url, parent=None):
        super().__init__(parent)
        self.mainWindow = mainWindow
        self.title = title
        self.url = url
        self.parent = parent

        self.setStyleSheet("""
            QToolBar{
                background-color: #31302f;
                font-size: 14px;
                padding: 5px;
            }
        """)

        open_url_btn = QPushButton(self.title)
        open_url_btn.setStyleSheet("""
        QPushButton {
            border-radius: 5px;
            background-color: #6E6E6D;
            padding: 3px;
            width: 200px
        }
        QPushButton:hover{
            background-color: #1E88E5;
        }
        """)
        open_url_btn.clicked.connect(lambda checked, url=self.url: self.open_bookmark(url))

        edit_btn = QPushButton(QIcon('icons/edit_black.png'), None, None)
        edit_btn.setIconSize(QSize(30, 30))
        edit_btn.setFixedSize(edit_btn.iconSize())
        delete_btn = QPushButton(QIcon('icons/delete_black.png'), None, None)
        delete_btn.setIconSize(QSize(30, 30))
        delete_btn.setFixedSize(delete_btn.iconSize())

        edit_btn.clicked.connect(self.edit_bookmark)
        delete_btn.clicked.connect(self.delete_bookmark)

        self.addWidget(open_url_btn)
        self.addWidget(edit_btn)
        self.addWidget(delete_btn)

    def open_bookmark(self, url):
        self.mainWindow.add_new_tab(QUrl(url))

    def edit_bookmark(self):
        # TODO - Implement the logic to edit the bookmark
        pass

    def delete_bookmark(self):
        self.parent.delete_bookmark(self.url)
        