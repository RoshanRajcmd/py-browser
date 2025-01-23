# importing required libraries
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtPrintSupport import *
from MainWindow import MainWindow
import sys

# creating a pyQt5 application
app = QApplication(sys.argv)

# setting name to the application
app.setApplicationName("Py Browser")

#app.setStyle("Fusion")
app.setWindowIcon(QtGui.QIcon('icons/pybrowser_icon.jpg'))

#styling tthe app
app.setStyleSheet("""
	QWidget{
		font-family: 'Segoe UI', sans-serif;
		font-size: 14px;			  
	}
	QStatusBar{
		border-radius: 5px;
		padding: 5px;
		background-color: #2196F3;
		color: white;
	}
	QMainWindow{
		background-color: #31302f;
		border-radius: 10px;
	}
""")

# creating a main window object
window = MainWindow(app)

# loop
app.exec_()
