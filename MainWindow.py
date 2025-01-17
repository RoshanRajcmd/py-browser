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
			json.dump([{'tile': HOME_TAB, 'url': GOOGLE}, {'tile': NEW_TAB, 'url': GOOGLE}], file, indent=4)
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
		tabBar = self.tabs.tabBar()
		tabBar.setStyleSheet("""
			QTabBar::close-button {
				subcontrol-position: right;
			}
			QTabBar::tab {
				height: 30px;
			}
		""")

		# Add a button to open a new tab
		self.newTabButton = QToolButton()
		self.newTabButton.setToolTip("Open a new tab")
		self.newTabButton.setIcon(QIcon("icons/add_black.png"))
		self.newTabButton.setIconSize(QSize(30, 30))
		#the size the icon should be same as the tabbar height else it will clip throught
		self.newTabButton.setFixedSize(self.newTabButton.iconSize())

	
		self.newTabButton.clicked.connect(lambda _: self.addNewTab())
		self.tabs.setCornerWidget(self.newTabButton, Qt.TopRightCorner)
		self.tabs.currentChanged.connect(self.currentTabChanged)
		self.tabs.tabCloseRequested.connect(self.closeCurrentTab)
		self.tabs.setStyleSheet("""
			# do not put the below style along with some other styles
			QTabBar::tab {
				max-width: 200px;
			}
		""")

		# creating a new tab
		self.addNewTab(QUrl(HOME_URL), 'Homepage')

		# set this tabs as central widget or main window
		self.setCentralWidget(self.tabs)

		# creating a status bar object
		self.status = QStatusBar()

		# adding status bar to the main window
		self.setStatusBar(self.status)

		# creating QToolBar for navigation
		navBar = QToolBar("Navigation")
		navBar.setMovable(False)

		# adding actions to the tool bar
		# creating a action for back
		backBtn = QPushButton(QIcon('icons/backward_black.png'), None, self)
		# setting status tip
		backBtn.setStatusTip("Back to previous page")
		# adding action to the back button
		# making currTab go back
		backBtn.clicked.connect(lambda: self.tabs.currentWidget().back())
		# adding this action to tool bar
		backBtn.setIconSize(QSize(30, 30))
		backBtn.setFixedSize(backBtn.iconSize())
		navBar.addWidget(backBtn)

		# similarly for forward action
		nextBtn = QPushButton(QIcon('icons/forward_black.png'), None, self)
		nextBtn.setStatusTip("Forward to next page")
		nextBtn.clicked.connect(lambda: self.tabs.currentWidget().forward())
		nextBtn.setIconSize(QSize(30, 30))
		nextBtn.setFixedSize(nextBtn.iconSize())
		navBar.addWidget(nextBtn)

		# similarly for reload action
		reloadBtn = QPushButton(QIcon('icons/refresh_black.png'), None, self)
		reloadBtn.setStatusTip("Reload page")
		reloadBtn.clicked.connect(lambda: self.tabs.currentWidget().reload())
		reloadBtn.setIconSize(QSize(30, 30))
		reloadBtn.setFixedSize(reloadBtn.iconSize())
		navBar.addWidget(reloadBtn)

		# similarly for home action
		homeBtn = QPushButton(QIcon('icons/home_black.png'), None, self)
		homeBtn.setStatusTip("Go home")
		homeBtn.clicked.connect(self.navigateHome)
		homeBtn.setIconSize(QSize(30, 30))
		homeBtn.setFixedSize(homeBtn.iconSize())
		navBar.addWidget(homeBtn)

		# adding stop action to the tool bar
		stopBtn = QPushButton(QIcon('icons/close_black.png'), None, self)
		stopBtn.setStatusTip("Stop loading current page")
		stopBtn.clicked.connect(lambda: self.tabs.currentWidget().stop())
		stopBtn.setIconSize(QSize(30, 30))
		stopBtn.setFixedSize(stopBtn.iconSize())
		navBar.addWidget(stopBtn)

		# adding a separator in the tool bar
		navBar.addSeparator()

		# creating a line edit for the url
		self.urlBar = QLineEdit('',navBar)

		#styling the URL bar
		self.urlBar.setStyleSheet("""
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
		self.urlBar.returnPressed.connect(self.navigateToUrl)

		# adding this to the tool bar
		navBar.addWidget(self.urlBar)

		bookmarkBtn = QPushButton(QIcon('icons/star_black'), None, self)
		bookmarkBtn.setStatusTip("Bookmark Page")
		bookmarkBtn.clicked.connect(self.addBookmark)
		bookmarkBtn.setIconSize(QSize(30, 30))
		bookmarkBtn.setFixedSize(bookmarkBtn.iconSize())
		navBar.addWidget(bookmarkBtn)

		actionBtn = QPushButton(QIcon('icons/menu_black'), None, self)
		actionBtn.setStatusTip("More Action")
		actionBtn.clicked.connect(self.showMoreActions)
		actionBtn.setIconSize(QSize(30, 30))
		actionBtn.setFixedSize(actionBtn.iconSize())
		navBar.addWidget(actionBtn)
		
         #customizing  the toolbare with rounded style
		navBar.setStyleSheet("""
			QToolBar{
				background-color: #31302f;
				font-size: 14px;
				padding: 5px;
			}
		""")

		# adding this tool bar tot he main window
		self.addToolBar(navBar)

		#Load in all the bookmarks
		self.bookmarks = self.loadBookmarks()

		# showing all the components
		self.show()

	def closeCurrentTab(self, i):
		if self.tabs.count() < 2:
			self.close()
			return
		self.tabs.removeTab(i)

	def addNewTab(self, qurl=None, label="Blank"):
		if qurl is None:
			qurl = QUrl(NEW_TAB_DEFAULT_URL)

		newTab = QWebEngineView()
		newTab.setUrl(qurl)
		i = self.tabs.addTab(newTab, label)
		self.tabs.setCurrentIndex(i)

		#Event listener to update URL, title and favicon
		newTab.urlChanged.connect(lambda qurl, newTab=newTab: self.updateUrlBar(qurl, newTab))
		newTab.loadStarted.connect(lambda i=i: self.updateTabLoadingIcon(i))
		newTab.loadFinished.connect(lambda _, i=i, newTab=newTab: self.updateTabTitleAndIcon(i, newTab))
		self.updateTitle()

	#Sets Loading icon when the page is loading
	def updateTabLoadingIcon(self, i):
			self.loadingIcon = QIcon('icons/loading_black.gif')
			self.tabs.setTabIcon(i, self.loadingIcon)

	def updateTabTitleAndIcon(self, i, currTab):
		page = currTab.page()
		icon = page.icon()
		title = page.title()
		self.tabs.setTabText(i, title)
		self.tabs.setTabIcon(i, icon)
		self.updateTitle()

	def currentTabChanged(self):
		qurl = self.tabs.currentWidget().url()
		self.updateUrlBar(qurl, self.tabs.currentWidget())
		self.updateTitle()

	# method for updating the title of the window
	def updateTitle(self):
		title = self.tabs.currentWidget().page().title()
		if len(title) > 25:
			title = title[:25] + "..."
		self.setWindowTitle("% s - Py Browser" % title)

	# method for updating url
	# this method is called by the QWebEngineView object
	def updateUrlBar(self, qurl, currTab=None):
		# print(qurl.toString())  # Debugging statement removed
		if currTab != self.tabs.currentWidget():
			return
		#self.urlBar.setText(qurl.toString())
		#self.urlBar.setCursorPosition(0)
		
	# method called by the home action
	def navigateHome(self):
		self.tabs.currentWidget().setUrl(QUrl(HOME_URL))
		self.updateTitle()

	# method called by the line edit when return key is pressed
	def navigateToUrl(self):
		qurl = QUrl(self.urlBar.text())
		if qurl.scheme() == "":
			qurl.setScheme("http")
		self.tabs.currentWidget().setUrl(qurl)

	def showMoreActions(self):
		dialog = ActionsDialog(self, self)

		#Position the dialog near the button
		#buttonPos = self.actionBtn.parentWidget().mapToGlobal(self.actionBtn.rect().bottomLeft())
		#dialog.move(buttonPos)

		#Show the dialog
		dialog.exec_()
	
	def loadBookmarks(self):
		if not os.path.exists(BOOKMARK_FILE):
			with open(BOOKMARK_FILE, 'w') as file:
				json.dump([{'tile': HOME_TAB, 'url': GOOGLE}, {'tile': NEW_TAB, 'url': GOOGLE}], file, indent=4)
			return []
		try:
			with open(BOOKMARK_FILE, 'r') as file:
				return json.load(file)
		except json.JSONDecodeError:
			# if file is empty or contains invalid JSON, return an empty list
			return []

	def addBookmark(self):
		webView = self.tabs.currentWidget()
		if webView and webView.url().toString():
			title = webView.page().title()
			bookmark = {'title': title, 'url': webView.url().toString()}
			self.bookmarks.append(bookmark)
			self.saveBookmark()
	
	def saveBookmark(self):
		# Save the bookmarks to the file
		with open(BOOKMARK_FILE, 'w') as file:
			json.dump(self.bookmarks, file, indent=4)