from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt5.QtCore import QUrl

class ActionsDialog(QDialog):
   
   def __init__(self, mainWindow, parent=None):
      super().__init__(parent)
      self.mainWindow = mainWindow
      self.bookmarks = self.mainWindow.bookmarks

      self.setWindowTitle("More Actions")
      self.setModal(False)

      self.layout = QVBoxLayout()

      self.viewBookMarksBtn = QPushButton("Show All BookMarks", self)
      self.viewBookMarksBtn.clicked.connect(self.viewBookMarksInTab)
      self.layout.addWidget(self.viewBookMarksBtn)
   
   def viewBookMarksInTab(self):
      dialog = QDialog(self)
      dialog.setWindowTitle("Bookmarks")
      layout = QVBoxLayout()

      for bookmark in self.bookmarks:
         button = QPushButton(bookmark['title'])
         button.clicked.connect(lambda checked, url=bookmark['url']: self.openBookMark(url))
         layout.addWidget(button)

      dialog.setLayout(layout)
      dialog.exec_()
   
   def openBookMark(self, url):
      self.mainWindow.addNewTab(QUrl(url))