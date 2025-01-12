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
		self.tabs.tabBarDoubleClicked.connect(self.tabOpenDoubleClick)
		self.tabs.currentChanged.connect(self.currentTabChanged)
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.closeCurrentTab)

		# creating a new tab
		self.addNewTab(QUrl('http://google.com'), 'Homepage')

		# set this tabs as central widget or main window
		self.setCentralWidget(self.tabs)

		# creating a status bar object
		self.status = QStatusBar()

		# adding status bar to the main window
		self.setStatusBar(self.status)

		# creating QToolBar for navigation
		navBar = QToolBar("Navigation")

		# adding actions to the tool bar
		# creating a action for back
		backBtn = QAction(QIcon('icons/backward_black.png'),"Back", self)
		# setting status tip
		backBtn.setStatusTip("Back to previous page")
		# adding action to the back button
		# making browser go back
		backBtn.triggered.connect(lambda: self.tabs.currentWidget().back())
		# adding this action to tool bar
		navBar.addAction(backBtn)

		# similarly for forward action
		nextBtn = QAction(QIcon('icons/forward_black.png'),"Forward", self)
		nextBtn.setStatusTip("Forward to next page")
		nextBtn.triggered.connect(lambda: self.tabs.currentWidget().forward())
		navBar.addAction(nextBtn)

		# similarly for reload action
		reloadBtn = QAction(QIcon('icons/reload_black.png'),"Reload", self)
		reloadBtn.setStatusTip("Reload page")
		reloadBtn.triggered.connect(lambda: self.tabs.currentWidget().reload())
		navBar.addAction(reloadBtn)

		# similarly for home action
		homeBtn = QAction(QIcon('icons/home_black.png'),"Home", self)
		homeBtn.setStatusTip("Go home")
		homeBtn.triggered.connect(self.navigate_home)
		navBar.addAction(homeBtn)

		# adding stop action to the tool bar
		stopBtn = QAction("X", self)
		stopBtn.setStatusTip("Stop loading current page")
		stopBtn.triggered.connect(lambda: self.tabs.currentWidget().stop())
		navBar.addAction(stopBtn)

		# adding a separator in the tool bar
		navBar.addSeparator()

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
		self.urlbar.returnPressed.connect(self.navigateToUrl)

		# adding this to the tool bar
		navBar.addWidget(self.urlbar)

		# creating a action for new tab
		# new_tab_btn = QAction(QIcon('icons/new_tab.png'), "New Tab", self)
		# new_tab_btn.setStatusTip("Open a new tab")
		# new_tab_btn.triggered.connect(lambda _: self.addNewTab())
		# navBar.addAction(new_tab_btn)

		bookmarkBtn = QAction(QIcon('icons/bookmark_black'),"Bookmark Page", self)
		bookmarkBtn.setStatusTip("Bookmark Page")
		#bookmarkBtn.triggered.connect(self.bookmarkPage)
		navBar.addAction(bookmarkBtn)

		actionBtn = QAction(QIcon('icons/bookmark_black'),"More Actions", self)
		actionBtn.setStatusTip("More Action")
		#actionBtn.triggered.connect(self.openActions)
		navBar.addAction(actionBtn)
		
                #customizing  the toolbare with rounded style
		navBar.setStyleSheet("""
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
		self.addToolBar(navBar)

		# showing all the components
		self.show()

	def addNewTab(self, qurl=None, label="Blank"):
		if qurl is None:
			qurl = QUrl('')

		browser = QWebEngineView()
		browser.setUrl(qurl)
		i = self.tabs.addTab(browser, label)
		self.tabs.setCurrentIndex(i)

		browser.urlChanged.connect(lambda qurl, browser=browser: self.updateUrlBar(qurl, browser))
		browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

	def tabOpenDoubleClick(self, i):
		if i == -1:
			self.addNewTab()

	def currentTabChanged(self, i):
		qurl = self.tabs.currentWidget().url()
		#self.updateUrlBar(qurl, self.tabs.currentWidget())
		self.updateTitle()

	def closeCurrentTab(self, i):
		if self.tabs.count() < 2:
			return
		self.tabs.removeTab(i)

	# method for updating the title of the window
	def updateTitle(self):
		title = self.tabs.currentWidget().page().title()
		self.setWindowTitle("% s - Py Browser" % title)

	# method called by the home action
	def navigate_home(self):
		self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

	# method called by the line edit when return key is pressed
	def navigateToUrl(self):
		q = QUrl(self.urlbar.text())
		if q.scheme() == "":
			q.setScheme("http")
		self.tabs.currentWidget().setUrl(q)

	# method for updating url
	# this method is called by the QWebEngineView object
	def updateUrlBar(self, q, browser=None):
		if browser != self.tabs.currentWidget():
			return
		self.urlbar.setText(q.toString())
		self.urlbar.setCursorPosition(0)
