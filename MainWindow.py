from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QToolBar, QAction, QLineEdit, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, Qt
import os

NEW_TAB_DEFAULT_URL = "http://www.google.com"
HOME_URL = "http://www.google.com"

# creating main window class
class MainWindow(QMainWindow):

	# constructor
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		# creating a QTabWidget
		self.tabs = QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.setTabsClosable(True)
		self.tabs.setTabPosition(QTabWidget.North)
		self.tabs.setTabShape(QTabWidget.Rounded)
		self.tabs.setMovable(True)
		self.tabs.setElideMode(Qt.ElideRight)
		self.tabs.setUsesScrollButtons(True)
		self.tabs.setTabBarAutoHide(False)
		#self.tabs.setTabCloseButtonPosition(QTabWidget.RightSide)
		self.tabs.tabBarDoubleClicked.connect(self.tabOpenDoubleClick)
		self.tabs.currentChanged.connect(self.currentTabChanged)
		self.tabs.tabCloseRequested.connect(self.closeCurrentTab)
		# self.tabs.setStyleSheet("""
		# 	QTabBar::tab {
		# 		height: 20px;
		# 	}
		# """)

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
		homeBtn.triggered.connect(self.navigateHome)
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
				background-color: #white;
				border-radius: 8px;
				width: 25px;
				height: 25px;
				margin: 0 5px;
			}
			QToolButton:hover{
				background-color: #ECEFF1;
			}
		""")

		# adding this tool bar tot he main window
		self.addToolBar(navBar)

		# showing all the components
		self.show()

	def tabOpenDoubleClick(self, i):
		if i == -1:
			self.addNewTab()

	def closeCurrentTab(self, i):
		if self.tabs.count() < 2:
			return
		self.tabs.removeTab(i)

	def addNewTab(self, qurl=None, label="Blank"):
		if qurl is None:
			qurl = QUrl(NEW_TAB_DEFAULT_URL)

		browser = QWebEngineView()
		browser.setUrl(qurl)
		i = self.tabs.addTab(browser, label)
		self.tabs.setCurrentIndex(i)

		browser.urlChanged.connect(lambda qurl, browser=browser: self.updateUrlBar(qurl, browser))
		browser.loadStarted.connect(lambda i=i: self.updateTabLoadingIcon(i))
		browser.loadFinished.connect(lambda _, i=i, browser=browser: self.updateTabTitleAndIcon(i, browser))
		self.updateTitle()

	#Sets Loading icon when the page is loading
	def updateTabLoadingIcon(self, i):
			self.loadingIcon = QIcon('icons/loading_black.gif')
			self.tabs.setTabIcon(i, self.loadingIcon)

	def updateTabTitleAndIcon(self, i, browser):
		page = browser.page()
		icon = page.icon()
		title = page.title()
		self.tabs.setTabText(i, title)
		self.tabs.setTabIcon(i, icon)
		self.updateTitle()

	def currentTabChanged(self, i):
		qurl = self.tabs.currentWidget().url()
		print("new URL: %s" % qurl)
		self.updateUrlBar(qurl, self.tabs.currentWidget())
		self.updateTitle()

	# method for updating the title of the window
	def updateTitle(self):
		# TODO - sometimes the page does not have a title when the app initialy started and when a new tab
		# TODO - the title gets updated only after you gone to the next page
		title = self.tabs.currentWidget().page().title()
		print("Titile: %s\n" % title)
		self.setWindowTitle("% s - Py Browser" % title)

	# method for updating url
	# this method is called by the QWebEngineView object
	def updateUrlBar(self, q, browser=None):
		if browser != self.tabs.currentWidget():
			return
		# TODO - The urlbar is not getting recognized as variable in the MainWindow
		#self.urlbar.setText(q)
		#self.urlbar.setText(str(q))
		#self.urlbar.setCursorPosition(0)
		
	# method called by the home action
	def navigateHome(self):
		self.tabs.currentWidget().setUrl(QUrl(HOME_URL))
		self.updateTitle()

	# method called by the line edit when return key is pressed
	def navigateToUrl(self):
		q = QUrl(self.urlbar.text())
		if q.scheme() == "":
			q.setScheme("http")
		self.tabs.currentWidget().setUrl(q)
