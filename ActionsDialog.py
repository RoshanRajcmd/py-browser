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

      # Set the layout to the dialog
      self.setLayout(self.layout)

      # Adjust the size of the dialog to fit its contents
      self.adjustSize()

      self.view_bookmark_btn = QPushButton("Show All BookMarks", self)
      self.view_bookmark_btn.setStyleSheet("""
        QPushButton {
            border-radius: 5px;
            background-color: #6E6E6D;
            padding: 3px;
         }
         QPushButton:hover{
            background-color: #1E88E5;
         }
      """)
      self.view_bookmark_btn.clicked.connect(self.view_bookmarks_in_tab)
      self.layout.addWidget(self.view_bookmark_btn)
   
   def view_bookmarks_in_tab(self):
      dialog = QDialog(self)
      dialog.setWindowTitle("Bookmarks")
      layout = QVBoxLayout()

      for bookmark in self.bookmarks:
         button = QPushButton(bookmark['title'])
         button.setStyleSheet("""
            QPushButton {
               border-radius: 5px;
               background-color: #6E6E6D;
               padding: 3px;
            }
            QPushButton:hover{
               background-color: #1E88E5;
            }
         """)
         button.clicked.connect(lambda checked, url=bookmark['url']: self.open_bookmark(url))
         layout.addWidget(button)

      dialog.setLayout(layout)
      dialog.exec_()
   
   def open_bookmark(self, url):
      self.mainWindow.add_new_tab(QUrl(url))