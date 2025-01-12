# importing required libraries
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from MainWindow import MainWindow
import sys

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
		background-color: #2196F3;
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
