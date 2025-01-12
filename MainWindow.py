from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QToolBar, QAction, QLineEdit, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
import os

# creating main window class
class MainWindow(QMainWindow):

	# constructor
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		# creating a QTabWidget
		self.tabs = QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
		self.tabs.currentChanged.connect(self.current_tab_changed)
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.close_current_tab)

		# creating a new tab
		self.add_new_tab(QUrl('http://google.com'), 'Homepage')

		# set this tabs as central widget or main window
		self.setCentralWidget(self.tabs)

		# creating a status bar object
		self.status = QStatusBar()

		# adding status bar to the main window
		self.setStatusBar(self.status)

		# creating QToolBar for navigation
		navtb = QToolBar("Navigation")

		# adding actions to the tool bar
		# creating a action for back
		back_btn = QAction(QIcon('icons/backward_black.png'),"Back", self)
		# setting status tip
		back_btn.setStatusTip("Back to previous page")
		# adding action to the back button
		# making browser go back
		back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
		# adding this action to tool bar
		navtb.addAction(back_btn)

		# similarly for forward action
		next_btn = QAction(QIcon('icons/forward_black.png'),"Forward", self)
		next_btn.setStatusTip("Forward to next page")
		next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
		navtb.addAction(next_btn)

		# similarly for reload action
		reload_btn = QAction(QIcon('icons/reload_black.png'),"Reload", self)
		reload_btn.setStatusTip("Reload page")
		reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
		navtb.addAction(reload_btn)

		# similarly for home action
		home_btn = QAction(QIcon('icons/home_black.png'),"Home", self)
		home_btn.setStatusTip("Go home")
		home_btn.triggered.connect(self.navigate_home)
		navtb.addAction(home_btn)

		# adding stop action to the tool bar
		stop_btn = QAction("X", self)
		stop_btn.setStatusTip("Stop loading current page")
		stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
		navtb.addAction(stop_btn)

		# adding a separator in the tool bar
		navtb.addSeparator()

		# creating a line edit for the url
		self.urlbar = QLineEdit(self)

		#styling the URL bar
		self.urlbar.setStyleSheet("""
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
		self.urlbar.returnPressed.connect(self.navigate_to_url)

		# adding this to the tool bar
		navtb.addWidget(self.urlbar)

		# creating a action for new tab
		# new_tab_btn = QAction(QIcon('icons/new_tab.png'), "New Tab", self)
		# new_tab_btn.setStatusTip("Open a new tab")
		# new_tab_btn.triggered.connect(lambda _: self.add_new_tab())
		# navtb.addAction(new_tab_btn)

		bookmark_btn = QAction(QIcon('icons/bookmark_black'),"Bookmark Page", self)
		bookmark_btn.setStatusTip("Bookmark Page")
		#bookmark_btn.triggered.connect(self.navigate_home)
		navtb.addAction(bookmark_btn)

		actions_btn = QAction(QIcon('icons/bookmark_black'),"More Actions", self)
		actions_btn.setStatusTip("More Action")
		#actions_btn.triggered.connect(self.navigate_home)
		navtb.addAction(actions_btn)
		
                #customizing  the toolbare with rounded style
		navtb.setStyleSheet("""
			QToolBar{
				background-color: #31302f;
				font-size: 14px;
				padding: 3px;
			}
			QToolButton{
				background-color: white;
				color: white;
				border-radius: 8px;
				width: 20px;
				height: 20px;
				margin: 0 5px;  # Adding uniform spacing between buttons
			}
			QToolButton:hover{
				background-color: #3e3d3c;
			}
		""")

		# adding this tool bar tot he main window
		self.addToolBar(navtb)

		# showing all the components
		self.show()

	def add_new_tab(self, qurl=None, label="Blank"):
		if qurl is None:
			qurl = QUrl('')

		browser = QWebEngineView()
		browser.setUrl(qurl)
		i = self.tabs.addTab(browser, label)
		self.tabs.setCurrentIndex(i)

		browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
		browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

	def tab_open_doubleclick(self, i):
		if i == -1:
			self.add_new_tab()

	def current_tab_changed(self, i):
		qurl = self.tabs.currentWidget().url()
		#self.update_urlbar(qurl, self.tabs.currentWidget())
		self.update_title()

	def close_current_tab(self, i):
		if self.tabs.count() < 2:
			return
		self.tabs.removeTab(i)

	# method for updating the title of the window
	def update_title(self):
		title = self.tabs.currentWidget().page().title()
		self.setWindowTitle("% s - Py Browser" % title)

	# method called by the home action
	def navigate_home(self):
		self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

	# method called by the line edit when return key is pressed
	def navigate_to_url(self):
		q = QUrl(self.urlbar.text())
		if q.scheme() == "":
			q.setScheme("http")
		self.tabs.currentWidget().setUrl(q)

	# method for updating url
	# this method is called by the QWebEngineView object
	def update_urlbar(self, q, browser=None):
		if browser != self.tabs.currentWidget():
			return
		self.urlbar.setText(q.toString())
		self.urlbar.setCursorPosition(0)
