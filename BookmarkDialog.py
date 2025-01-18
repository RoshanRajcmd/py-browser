from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox

class BookmarkDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        #Set up dialog properties
        self.setWindowTitle("Add Bookmark")
        self.setModal(False)

        #create the form layout
        self.layout = QFormLayout()

        #Add fields for title and URL
        self.title_input = QLineEdit(self)
        self.url_input = QLineEdit(self)
        self.layout.addRow("Title:", self.title_input)
        self.layout.addRow("URL:", self.url_input)

        #add standard buttons (OK and cancel)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.layout.addWidget(self.buttons)

        #Connect the button signals
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_input(self):
        return self.title_input.text(), self.url_input.text()
