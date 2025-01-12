# importing required libraries
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QStatusBar, QToolBar, QAction, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import *
import os
import sys

# creating main window class
class MainWindow(QMainWindow):

	# constructor
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)


		# creating a QWebEngineView
		self.browser = QWebEngineView()

		# setting default browser url as google
		self.browser.setUrl(QUrl("http://google.com"))

		# adding action when url get changed
		self.browser.urlChanged.connect(self.update_urlbar)

		# adding action when loading is finished
		self.browser.loadFinished.connect(self.update_title)

		# set this browser as central widget or main window
		self.setCentralWidget(self.browser)

		# creating a status bar object
		self.status = QStatusBar()

		# adding status bar to the main window
		self.setStatusBar(self.status)

		# creating QToolBar for navigation
		navtb = QToolBar("Navigation")
		
        #customizing  the toolbare with rounded style
		navtb.setStyleSheet("""
            QToolBar{
                background-color: #5C6BC0;
                border-radius: 10px;
                font-size: 14px;
                padding: 5px;
            }
            QToolButton{
                background-color: #3F51B5;
                color: white;
                border-radius: 8px;
                padding: 8px;
            }
            QToolButton:hover{
                background-color: #1E88E5;
            }
        """)

		# adding this tool bar tot he main window
		self.addToolBar(navtb)

		# adding actions to the tool bar
		# creating a action for back
		back_btn = QAction(QIcon('icons/backward.png'),"Back", self)
		# setting status tip
		back_btn.setStatusTip("Back to previous page")
		# adding action to the back button
		# making browser go back
		back_btn.triggered.connect(self.browser.back)
		# adding this action to tool bar
		navtb.addAction(back_btn)

		# similarly for forward action
		next_btn = QAction(QIcon('icons/forward.png'),"Forward", self)
		next_btn.setStatusTip("Forward to next page")
		next_btn.triggered.connect(self.browser.forward)
		navtb.addAction(next_btn)

		# similarly for reload action
		reload_btn = QAction(QIcon('icons/forward.png'),"Reload", self)
		reload_btn.setStatusTip("Reload page")
		reload_btn.triggered.connect(self.browser.reload)
		navtb.addAction(reload_btn)

		# similarly for home action
		home_btn = QAction(QIcon('icons/forward.png'),"Home", self)
		home_btn.setStatusTip("Go home")
		home_btn.triggered.connect(self.navigate_home)
		navtb.addAction(home_btn)

		# adding a separator in the tool bar
		navtb.addSeparator()

		# creating a line edit for the url
		self.urlbar = QLineEdit()

		#styling the URL bar
		self.urlbar.setStyleSheet("""
			QLineEdit{
				border-radius: 15px;
				padding: 5px;
				background-color: white;
				font-size: 14px;
				color: #808080;
			}
			QLineEdit:focus{
				border: 2px solid #1E88E5;
			}
		""")

		# adding action when return key is pressed
		self.urlbar.returnPressed.connect(self.navigate_to_url)

		# adding this to the tool bar
		navtb.addWidget(self.urlbar)

		# adding stop action to the tool bar
		stop_btn = QAction(QIcon('icons/forward.png'),"Stop", self)
		stop_btn.setStatusTip("Stop loading current page")
		stop_btn.triggered.connect(self.browser.stop)
		navtb.addAction(stop_btn)

		# showing all the components
		self.show()


	# method for updating the title of the window
	def update_title(self):
		title = self.browser.page().title()
		self.setWindowTitle("% s - Py Browser" % title)


	# method called by the home action
	def navigate_home(self):

		# open the google
		self.browser.setUrl(QUrl("http://www.google.com"))

	# method called by the line edit when return key is pressed
	def navigate_to_url(self):

		# getting url and converting it to QUrl object
		q = QUrl(self.urlbar.text())

		# if url is scheme is blank
		if q.scheme() == "":
			# set url scheme to html
			q.setScheme("http")

		# set the url to the browser
		self.browser.setUrl(q)

	# method for updating url
	# this method is called by the QWebEngineView object
	def update_urlbar(self, q):

		# setting text to the url bar
		self.urlbar.setText(q.toString())

		# setting cursor position of the url bar
		self.urlbar.setCursorPosition(0)


# creating a pyQt5 application
app = QApplication(sys.argv)

# setting name to the application
app.setApplicationName("Py Browser")

#styling tthe app
app.setStyleSheet("""
	QWidget{
		font-family: 'Segoe UI', sans-serif;
		font-size: 14px;			  
	}
	QStatusBar{
		border-radius: 5px;
		padding: 5px;
		background-color:#2196F3;
		color: white;
	}
	QMainWindow{
		background-color: #ECEFF1;
		border-radius: 10px;
	}
""")

# creating a main window object
window = MainWindow()

# loop
app.exec_()
