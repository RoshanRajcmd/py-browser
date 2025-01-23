from PyQt5.QtWidgets import QPushButton, QToolBar, QLineEdit, QHBoxLayout, QWidget
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon
from utils import HOME_TAB, NEW_TAB

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

        self.open_url_btn = QPushButton(self.title)
        self.open_url_btn.setStyleSheet("""
        QPushButton {
            border-radius: 5px;
            background-color: #6E6E6D;
            padding: 3px;
            width: 250px
        }
        QPushButton:hover{
            background-color: #1E88E5;
        }
        """)
        self.open_url_btn.clicked.connect(lambda checked, url=self.url: self.open_bookmark(url))
        self.addWidget(self.open_url_btn)

        self.edit_btn = QPushButton(QIcon('icons/edit_black.png'), None, None)
        self.edit_btn.setIconSize(QSize(30, 30))
        self.edit_btn.setFixedSize(self.edit_btn.iconSize())
        self.edit_btn.clicked.connect(self.edit_bookmark)
        self.addWidget(self.edit_btn)

        if self.title not in [HOME_TAB, NEW_TAB]:
            self.delete_btn = QPushButton(QIcon('icons/delete_black.png'), None, None)
            self.delete_btn.setIconSize(QSize(30, 30))
            self.delete_btn.setFixedSize(self.delete_btn.iconSize())
            self.delete_btn.clicked.connect(self.delete_bookmark)
            self.addWidget(self.delete_btn)

    def open_bookmark(self, url):
        self.mainWindow.add_new_tab(QUrl(url))

    def edit_bookmark(self):
        self.layout = QHBoxLayout()
        self.title_edit = QLineEdit(self.title)
        self.title_edit.setStyleSheet("""
            QLineEdit{
            border-radius: 5px;
            padding: 3px;
            background-color: black;
            font-size: 14px;
            color: white;
            width: 150px;
            }
            QLineEdit:focus{
            border: 2px solid #1E88E5;
            }
        """)
        if self.title in [HOME_TAB, NEW_TAB]:
            self.title_edit.setReadOnly(True)
        self.url_edit = QLineEdit(self.url)
        self.url_edit.setStyleSheet("""
            QLineEdit{
            border-radius: 5px;
            padding: 3px;
            background-color: black;
            font-size: 14px;
            color: white;
            width: 150px;
            }
            QLineEdit:focus{
            border: 2px solid #1E88E5;
            }
        """)
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_edited_bookmark)

        self.layout.addWidget(self.title_edit)
        self.layout.addWidget(self.url_edit)
        self.layout.addWidget(self.save_btn)

        self.edit_widget = QWidget()
        self.edit_widget.setLayout(self.layout)

        self.clear()
        self.addWidget(self.edit_widget)

    def save_edited_bookmark(self):
        new_title = self.title_edit.text()
        new_url = self.url_edit.text()

        # Update the bookmark in the main window
        for bookmark in self.mainWindow.bookmarks:
            if bookmark['url'] == self.url and bookmark['title'] == self.title:
                bookmark['title'] = new_title
                bookmark['url'] = new_url
                break

        self.parent.save_bookmark()

        # Update the current bookmark bar
        self.title = new_title
        self.url = new_url

        self.clear()
        self.addWidget(self.open_url_btn)
        self.addWidget(self.edit_btn)
        if self.title not in [HOME_TAB, NEW_TAB]:
            self.addWidget(self.delete_btn)

    def delete_bookmark(self):
        self.parent.delete_bookmark(self.url)
