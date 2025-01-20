from PyQt5.QtWidgets import QToolBar, QPushButton, QMenu, QAction, QVBoxLayout, QDialog, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QUrl
from SelectableLineEdit import SelectableLineEdit
from BookmarkDialog import BookmarkDialog
import json
from utils import BOOKMARK_FILE

class NavBar(QToolBar):
    def __init__(self, mainWindow, parent=None):
        super().__init__(parent)
        self.mainWindow = mainWindow
        
        # adding actions to the tool bar
        # creating a action for back
        back_btn = QPushButton(QIcon('icons/backward_black.png'), None, self)
        # setting status tip
        back_btn.setStatusTip("Back to previous page")
        # adding action to the back button
        # making currTab go back
        back_btn.clicked.connect(lambda: self.mainWindow.tabs.currentWidget().back())
        # adding this action to tool bar
        back_btn.setIconSize(QSize(30, 30))
        back_btn.setFixedSize(back_btn.iconSize())
        self.addWidget(back_btn)

        # similarly for forward action
        next_btn = QPushButton(QIcon('icons/forward_black.png'), None, self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.clicked.connect(lambda: self.mainWindow.tabs.currentWidget().forward())
        next_btn.setIconSize(QSize(30, 30))
        next_btn.setFixedSize(next_btn.iconSize())
        self.addWidget(next_btn)

        # similarly for reload action
        reload_btn = QPushButton(QIcon('icons/refresh_black.png'), None, self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.clicked.connect(lambda: self.mainWindow.tabs.currentWidget().reload())
        reload_btn.setIconSize(QSize(30, 30))
        reload_btn.setFixedSize(reload_btn.iconSize())
        self.addWidget(reload_btn)

        # similarly for home action
        home_btn = QPushButton(QIcon('icons/home_black.png'), None, self)
        home_btn.setStatusTip("Go home")
        home_btn.clicked.connect(self.mainWindow.navigate_home)
        home_btn.setIconSize(QSize(30, 30))
        home_btn.setFixedSize(home_btn.iconSize())
        self.addWidget(home_btn)

        # adding stop action to the tool bar
        stop_btn = QPushButton(QIcon('icons/close_black.png'), None, self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.clicked.connect(lambda: self.mainWindow.tabs.currentWidget().stop())
        stop_btn.setIconSize(QSize(30, 30))
        stop_btn.setFixedSize(stop_btn.iconSize())
        self.addWidget(stop_btn)

        # adding a separator in the tool bar
        self.addSeparator()

        # creating a line edit for the url
        self.url_bar = SelectableLineEdit('', self)
        #self.url_bar = QLineEdit('', self)

        #styling the URL bar
        self.url_bar.setStyleSheet("""
            QLineEdit{
                border-radius: 13px;
                padding: 5px;
                background-color: black;
                font-size: 14px;
                color: white;
            }
            QLineEdit:focus{
                border: 2px solid #1E88E5;
            }
        """)

        # adding action when return key is pressed
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # adding this to the tool bar
        self.addWidget(self.url_bar)

        self.bookmark_btn = QPushButton(None, self)
        self.bookmark_btn.setStyleSheet("""
            QPushButton{
                background-color: #ffffff;
                border-radius: 5px;	
            }				  
        """)
        self.check_change_bookmark_icon(None)
        self.bookmark_btn.setStatusTip("Bookmark Page")
        self.bookmark_btn.clicked.connect(self.add_bookmark)
        self.bookmark_btn.setIconSize(QSize(30, 30))
        self.bookmark_btn.setFixedSize(self.bookmark_btn.iconSize())
        self.addWidget(self.bookmark_btn)

        self.action_btn = QPushButton(QIcon('icons/menu_black'), None, self)
        self.action_btn.setStatusTip("More Action")
        self.menu = QMenu(self)
        self.show_all_bookmark = QAction("Show All Bookmarks" ,self)
        self.show_all_bookmark.triggered.connect(self.view_bookmarks_in_tab)
        self.menu.addAction(self.show_all_bookmark)
        self.action_btn.setMenu(self.menu)
        self.action_btn.setIconSize(QSize(30, 30))
        self.action_btn.setFixedSize(self.action_btn.iconSize())
        self.addWidget(self.action_btn)

        #customizing  the toolbare with rounded style
        self.setStyleSheet("""
            QToolBar{
                background-color: #31302f;
                font-size: 14px;
                padding: 5px;
            }
        """)

    def get_bookmark_btn(self):
        return self.bookmark_btn
    
    def get_url_bar(self):
        return self.url_bar

    # method called by the line edit when return key is pressed
    def navigate_to_url(self):
        qurl = QUrl(self.url_bar.text())
        if qurl.scheme() == "":
            qurl.setScheme("http")
        self.mainWindow.tabs.currentWidget().setUrl(qurl)
        self.check_change_bookmark_icon(qurl)

    def add_bookmark(self):
        #Get the current tab Title and URL 
        web_view = self.mainWindow.tabs.currentWidget()
        if web_view and web_view.url().toString() and web_view.page().title():
            dialog = BookmarkDialog(web_view.page().title(), web_view.url().toString(), self)

        #if the dialog executed 
        if dialog.exec_() == QDialog.Accepted:
            title, url = dialog.get_input()
            print("Bookmark added: Title = {title}, URL = {url}")
        
            #add them to the bookmarks.json
            bookmark = {'title': title, 'url': url}
            self.mainWindow.bookmarks.append(bookmark)
            self.save_bookmark()
            # self.bookmark_btn = QPushButton(QIcon('icons/star_white'), None, self)
            # self.bookmark_btn.repaint()
            self.check_change_bookmark_icon(web_view.url())
        elif dialog.exec_() == QDialog.Rejected:
            return

    def view_bookmarks_in_tab(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Bookmarks")
        layout = QVBoxLayout()

        for bookmark in self.mainWindow.bookmarks:
            button = QPushButton(bookmark['title'])
            button.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #6E6E6D;
                padding: 3px;
            }
            QPushButton:hover{
                background-color: #1E88E5;
            }
            """)
            button.clicked.connect(lambda checked, url=bookmark['url']: self.open_bookmark(url))
            layout.addWidget(button)

        dialog.setLayout(layout)
        dialog.exec_()

    def open_bookmark(self, url):
        self.mainWindow.add_new_tab(QUrl(url))

    def check_change_bookmark_icon(self, qurl):
        # Check if the current page URL is one of the URLs in bookmarks.json file
        if qurl is None:
            self.bookmark_btn.setIcon(QIcon('icons/star_black'))
            # Refresh the button to apply the change
            self.bookmark_btn.repaint()
            return
        
        for bookmark in self.mainWindow.bookmarks:
            if bookmark['url'] == qurl.toString():
                self.bookmark_btn.setIcon(QIcon('icons/star_white'))
                self.bookmark_btn.repaint()
                break
        else:
            self.bookmark_btn.setIcon(QIcon('icons/star_black'))
            self.bookmark_btn.repaint() 

    def save_bookmark(self):
        # Save the bookmarks to the file
        with open(BOOKMARK_FILE, 'w') as file:
            json.dump(self.mainWindow.bookmarks, file, indent=4) 