from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QToolBar, QLineEdit, QTabWidget, QToolButton, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, Qt, QSize
from ActionsDialog import ActionsDialog
import os
import json

BOOKMARK_FILE = "/Users/roshanraj-mac/Documents/VSCodeWS/py-browser/bookmarks.json"
HOME_TAB = "home_tab_title"
NEW_TAB = "new_tab_title"
GOOGLE = "http://www.google.com"

#Search and Loads up the Home url and new tab url from bookmarks.json
def load_urls_from_bookmarks():
	#If there is no bookmark.json create one with default tab urls in it
	if not os.path.exists(BOOKMARK_FILE):
		with open(BOOKMARK_FILE, 'w') as file:
			json.dump([{'title': HOME_TAB, 'url': GOOGLE}, {'title': NEW_TAB, 'url': GOOGLE}], file, indent=4)
		return GOOGLE, GOOGLE
	try:
		with open(BOOKMARK_FILE, 'r') as file:
			bookmarks = json.load(file)
			home_url = next((bookmark['url'] for bookmark in bookmarks if bookmark['title'] == HOME_TAB), GOOGLE)
			new_tab_url = next((bookmark['url'] for bookmark in bookmarks if bookmark['title'] == NEW_TAB), GOOGLE)
			return home_url, new_tab_url
	except json.JSONDecodeError:
		return GOOGLE, GOOGLE

HOME_URL, NEW_TAB_DEFAULT_URL = load_urls_from_bookmarks()

# creating main window class
class MainWindow(QMainWindow):

	# constructor
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

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
		self.tabs.currentChanged.connect(self.current_tab_changed)
		self.tabs.tabCloseRequested.connect(self.close_current_tab)
		self.tabs.setStyleSheet("""
			# do not put the below style along with some other styles
			QTabBar::tab {
				max-width: 200px;
			}
		""")

		# creating a new tab
		self.add_new_tab(QUrl(HOME_URL), 'Homepage')

		# set this tabs as central widget or main window
		self.setCentralWidget(self.tabs)

		# creating a status bar object
		self.status = QStatusBar()

		# adding status bar to the main window
		self.setStatusBar(self.status)

		# creating QToolBar for navigation
		nav_bar = QToolBar("Navigation")
		nav_bar.setMovable(False)

		# adding actions to the tool bar
		# creating a action for back
		back_btn = QPushButton(QIcon('icons/backward_black.png'), None, self)
		# setting status tip
		back_btn.setStatusTip("Back to previous page")
		# adding action to the back button
		# making currTab go back
		back_btn.clicked.connect(lambda: self.tabs.currentWidget().back())
		# adding this action to tool bar
		back_btn.setIconSize(QSize(30, 30))
		back_btn.setFixedSize(back_btn.iconSize())
		nav_bar.addWidget(back_btn)

		# similarly for forward action
		next_btn = QPushButton(QIcon('icons/forward_black.png'), None, self)
		next_btn.setStatusTip("Forward to next page")
		next_btn.clicked.connect(lambda: self.tabs.currentWidget().forward())
		next_btn.setIconSize(QSize(30, 30))
		next_btn.setFixedSize(next_btn.iconSize())
		nav_bar.addWidget(next_btn)

		# similarly for reload action
		reload_btn = QPushButton(QIcon('icons/refresh_black.png'), None, self)
		reload_btn.setStatusTip("Reload page")
		reload_btn.clicked.connect(lambda: self.tabs.currentWidget().reload())
		reload_btn.setIconSize(QSize(30, 30))
		reload_btn.setFixedSize(reload_btn.iconSize())
		nav_bar.addWidget(reload_btn)

		# similarly for home action
		home_btn = QPushButton(QIcon('icons/home_black.png'), None, self)
		home_btn.setStatusTip("Go home")
		home_btn.clicked.connect(self.navigate_home)
		home_btn.setIconSize(QSize(30, 30))
		home_btn.setFixedSize(home_btn.iconSize())
		nav_bar.addWidget(home_btn)

		# adding stop action to the tool bar
		stop_btn = QPushButton(QIcon('icons/close_black.png'), None, self)
		stop_btn.setStatusTip("Stop loading current page")
		stop_btn.clicked.connect(lambda: self.tabs.currentWidget().stop())
		stop_btn.setIconSize(QSize(30, 30))
		stop_btn.setFixedSize(stop_btn.iconSize())
		nav_bar.addWidget(stop_btn)

		# adding a separator in the tool bar
		nav_bar.addSeparator()

		# creating a line edit for the url
		self.url_bar = QLineEdit('', nav_bar)

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
		nav_bar.addWidget(self.url_bar)

		bookmark_btn = QPushButton(QIcon('icons/star_black'), None, self)
		bookmark_btn.setStatusTip("Bookmark Page")
		bookmark_btn.clicked.connect(self.add_bookmark)
		bookmark_btn.setIconSize(QSize(30, 30))
		bookmark_btn.setFixedSize(bookmark_btn.iconSize())
		nav_bar.addWidget(bookmark_btn)

		action_btn = QPushButton(QIcon('icons/menu_black'), None, self)
		action_btn.setStatusTip("More Action")
		action_btn.clicked.connect(self.show_more_actions)
		action_btn.setIconSize(QSize(30, 30))
		action_btn.setFixedSize(action_btn.iconSize())
		nav_bar.addWidget(action_btn)

		#customizing  the toolbare with rounded style
		nav_bar.setStyleSheet("""
			QToolBar{
				background-color: #31302f;
				font-size: 14px;
				padding: 5px;
			}
		""")

		# adding this tool bar tot he main window
		self.addToolBar(nav_bar)

		#Load in all the bookmarks
		self.bookmarks = self.load_bookmarks()

		# showing all the components
		self.show()

	def close_current_tab(self, i):
		if self.tabs.count() < 2:
			self.close()
			return
		self.tabs.removeTab(i)

	def add_new_tab(self, qurl=None, label="Blank"):
		if qurl is None:
			qurl = QUrl(NEW_TAB_DEFAULT_URL)

		new_tab = QWebEngineView()
		new_tab.setUrl(qurl)
		i = self.tabs.addTab(new_tab, label)
		self.tabs.setCurrentIndex(i)

		#Event listener to update URL, title and favicon
		new_tab.urlChanged.connect(lambda qurl, new_tab=new_tab: self.update_url_bar(qurl, new_tab))
		new_tab.loadStarted.connect(lambda i=i: self.update_tab_loading_icon(i))
		new_tab.loadFinished.connect(lambda _, i=i, new_tab=new_tab: self.update_tab_title_and_icon(i, new_tab))
		self.update_title()

	#Sets Loading icon when the page is loading
	def update_tab_loading_icon(self, i):
		self.loading_icon = QIcon('icons/loading_black.gif')
		self.tabs.setTabIcon(i, self.loading_icon)

	def update_tab_title_and_icon(self, i, curr_tab):
		page = curr_tab.page()
		icon = page.icon()
		title = page.title()
		self.tabs.setTabText(i, title)
		self.tabs.setTabIcon(i, icon)
		self.update_title()

	def current_tab_changed(self):
		qurl = self.tabs.currentWidget().url()
		self.update_url_bar(qurl, self.tabs.currentWidget())
		self.update_title()

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
		#self.urlBar.setText(qurl.toString())
		#self.urlBar.setCursorPosition(0)

	# method called by the home action
	def navigate_home(self):
		self.tabs.currentWidget().setUrl(QUrl(HOME_URL))
		self.update_title()

	# method called by the line edit when return key is pressed
	def navigate_to_url(self):
		qurl = QUrl(self.url_bar.text())
		if qurl.scheme() == "":
			qurl.setScheme("http")
		self.tabs.currentWidget().setUrl(qurl)

	def show_more_actions(self):
		dialog = ActionsDialog(self, self)
		#Position the dialog near the button
		#buttonPos = self.actionBtn.parentWidget().mapToGlobal(self.actionBtn.rect().bottomLeft())
		#dialog.move(buttonPos)

		#Show the dialog
		dialog.exec_()

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

	def add_bookmark(self):
		web_view = self.tabs.currentWidget()
		if web_view and web_view.url().toString():
			title = web_view.page().title()
			bookmark = {'title': title, 'url': web_view.url().toString()}
			self.bookmarks.append(bookmark)
			self.save_bookmark()

	def save_bookmark(self):
		# Save the bookmarks to the file
		with open(BOOKMARK_FILE, 'w') as file:
			json.dump(self.bookmarks, file, indent=4)
