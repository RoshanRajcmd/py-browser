from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton

class ActionsDialog(QDialog):
   
   def __init__(self, parent=None):
      super().__init__(parent)

      self.setWindowTitle("More Actions")
      self.setModal(True)

      self.layout = QVBoxLayout()

      self.viewBookMarksBtn = QPushButton()
      self.viewBookMarksBtn.clicked.connect(self.viewBookMarksInTab)
      self.layout.addWidget(self.viewBookMarksBtn)
   
   def viewBookMarksInTab(self):
      dialog = QDialog(self)
      dialog.setWindowTitle("Bookmarks")
      layout = QVBoxLayout()