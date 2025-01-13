from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QToolBar, QAction, QLineEdit, QTabWidget, QToolButton
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
		self.tabs.setMovable(True)
		self.tabs.setTabPosition(QTabWidget.North)
		#contols the size of tab bar to be dynamic when there is no enough space
		self.tabs.setElideMode(Qt.ElideRight)
		self.tabs.setUsesScrollButtons(True)
		tabBar = self.tabs.tabBar()
		tabBar.setStyleSheet("""
			QTabBar::close-button {
				subcontrol-position: right;
			}
		""")

		# Add a button to open a new tab
		self.newTabButton = QToolButton()
		self.newTabButton.setIcon(QIcon("icons/image.png"))
		self.newTabButton.setToolTip("Open a new tab")
		self.newTabButton.clicked.connect(lambda _: self.addNewTab())
		self.tabs.setCornerWidget(self.newTabButton, Qt.TopRightCorner)
		self.tabs.currentChanged.connect(self.currentTabChanged)
		self.tabs.tabCloseRequested.connect(self.closeCurrentTab)
		self.tabs.setStyleSheet("""
			# do not put the below style along with some other styles
			QTabBar::tab {
				max-width: 200px;
			}
			QToolButton{
				background-color: 31302f;
			}
		""")

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
		# making currTab go back
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
				background-color: #31302f;
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
		print(qurl.toString())
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
