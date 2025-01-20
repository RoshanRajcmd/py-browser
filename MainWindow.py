from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QTabWidget, QToolButton, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, Qt, QSize
from NavBar import NavBar
from utils import load_urls_from_bookmarks, BOOKMARK_FILE, HOME_TAB, NEW_TAB, GOOGLE
import os
import json

HOME_URL, NEW_TAB_DEFAULT_URL = load_urls_from_bookmarks()

# creating main window class
class MainWindow(QMainWindow):

	# constructor
	def __init__(self, app, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.app = app

		#Load in all the bookmarks
		self.bookmarks = self.load_bookmarks()

		# creating a QTabWidget
		self.tabs = QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.setTabsClosable(True)
		self.tabs.setMovable(True)
		self.tabs.setTabPosition(QTabWidget.North)
		# controls the size of tab bar to be dynamic when there is no enough space
		self.tabs.setElideMode(Qt.ElideRight)
		self.tabs.setUsesScrollButtons(True)
		tab_bar = self.tabs.tabBar()
		tab_bar.setStyleSheet("""
			QTabBar::close-button {
				subcontrol-position: right;
			}
			QTabBar::tab {
				height: 30px;
			}
		""")

		# Add a button to open a new tab
		self.new_tab_button = QToolButton()
		self.new_tab_button.setToolTip("Open a new tab")
		self.new_tab_button.setIcon(QIcon("icons/add_black.png"))
		self.new_tab_button.setIconSize(QSize(30, 30))
		#the size the icon should be same as the tabbar height else it will clip throught
		self.new_tab_button.setFixedSize(self.new_tab_button.iconSize())

		self.new_tab_button.clicked.connect(lambda _: self.add_new_tab())
		self.tabs.setCornerWidget(self.new_tab_button, Qt.TopRightCorner)
		self.tabs.tabCloseRequested.connect(self.close_current_tab)
		self.tabs.setStyleSheet("""
			# do not put the below style along with some other styles
			QTabBar::tab {
				max-width: 200px;
			}
		""")

		# set this tabs as central widget or main window
		self.setCentralWidget(self.tabs)

		# creating QToolBar for navigation
		self.nav_bar = NavBar(self, self)
		self.nav_bar.setMovable(False)

		# adding this tool bar tot he main window
		self.addToolBar(self.nav_bar)

		# creating a status bar object
		self.status = QStatusBar()
		# adding status bar to the main window
		self.setStatusBar(self.status)

 		# Do not change the order of the below lines - Let it be as it is
		 
		# Connect the currentChanged signal after url_bar is defined
		# The below line need to be here else the method current_tab_changed cannot recognize the self.url_bar of the MainWindow
		self.tabs.currentChanged.connect(self.current_tab_changed)

		# creating a new tab
		self.add_new_tab(QUrl(HOME_URL), 'Homepage')

		# showing all the components
		self.show()

	def close_current_tab(self, i):
		if self.tabs.count() <= 1:
			#quit via the App instance
			self.app.quit()
			return
		self.tabs.removeTab(i)

	def add_new_tab(self, qurl=None, label="Blank"):
		if qurl is None:
			qurl = QUrl(NEW_TAB_DEFAULT_URL)

		new_tab = QWebEngineView()
		new_tab.setUrl(qurl)
		i = self.tabs.addTab(new_tab, label)
		self.tabs.setCurrentIndex(i)

		# Event listener to update URL, title and favicon
		new_tab.urlChanged.connect(lambda qurl, new_tab=new_tab: self.update_url_bar(qurl, new_tab))
		new_tab.loadStarted.connect(lambda i=i: self.update_tab_loading_icon(i))
		new_tab.loadFinished.connect(lambda _, i=i, new_tab=new_tab: self.update_tab_title_and_icon(i, new_tab))
		new_tab.iconChanged.connect(lambda icon, i=i: self.tabs.setTabIcon(i, icon))
		self.update_title()
		self.nav_bar.check_change_bookmark_icon(qurl)

	#Sets Loading icon when the page is loading
	def update_tab_loading_icon(self, i):
		self.loading_icon = QIcon('icons/loading_black.gif')
		self.tabs.setTabIcon(i, self.loading_icon)

	#update the page title ad favicon from the page it got loaded
	def update_tab_title_and_icon(self, i, curr_tab):
		page = curr_tab.page()
		icon = page.icon()
		title = page.title()
		self.tabs.setTabText(i, title)
		self.tabs.setTabIcon(i, icon)
		self.update_title()
		self.nav_bar.check_change_bookmark_icon(page.url())

	def current_tab_changed(self):
		if self.tabs.count() == 0:
			return
		qurl = self.tabs.currentWidget().url()
		self.update_url_bar(qurl, self.tabs.currentWidget())
		self.update_title()
		self.nav_bar.check_change_bookmark_icon(qurl)
		self.nav_bar.get_bookmark_btn().repaint()

	# method for updating the title of the window
	def update_title(self):
		title = self.tabs.currentWidget().page().title()
		if len(title) > 25:
			title = title[:25] + "..."
		self.setWindowTitle("% s - Py Browser" % title)

	# method for updating url
	# this method is called by the QWebEngineView object
	def update_url_bar(self, qurl, curr_tab=None):
		# print(qurl.toString())  # Debugging statement removed
		if curr_tab != self.tabs.currentWidget():
			return
		self.nav_bar.get_url_bar().setText(qurl.toString())
		self.nav_bar.get_url_bar().setCursorPosition(0)

	def load_bookmarks(self):
		if not os.path.exists(BOOKMARK_FILE):
			with open(BOOKMARK_FILE, 'w') as file:
				json.dump([{'title': HOME_TAB, 'url': GOOGLE}, {'title': NEW_TAB, 'url': GOOGLE}], file, indent=4)
			return []
		try:
			with open(BOOKMARK_FILE, 'r') as file:
				return json.load(file)
		except json.JSONDecodeError:
			# if file is empty or contains invalid JSON, return an empty list
			return []
	
	# method called by the home action
	def navigate_home(self):
		self.tabs.currentWidget().setUrl(QUrl(HOME_URL))
		self.update_title()