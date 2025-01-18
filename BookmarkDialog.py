from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox

class BookmarkDialog(QDialog):

    def __init__(self, title, url, parent=None):
        super().__init__(parent)

        #Set up dialog properties
        self.setWindowTitle("Add Bookmark")

        #create the form layout
        self.layout = QFormLayout()

        #Add fields for title and URL
        self.title_input = QLineEdit(self)
        self.url_input = QLineEdit(self)
        self.title_input.setText(title)
        self.url_input.setText(url)
        self.layout.addRow("Title:", self.title_input)
        self.layout.addRow("URL:", self.url_input)

        # Set the layout to the dialog
        self.setLayout(self.layout)

        # Adjust the size of the dialog to fit its contents
        self.adjustSize()

        #add standard buttons (OK and cancel)
        # Combine OK and Cancel buttons using bitwise OR operator
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        # Connect the OK button to the accept method, which closes the dialog and returns QDialog.Accepted
        self.buttons.accepted.connect(self.accept)
        # Connect the Cancel button to the reject method, which closes the dialog and returns QDialog.Rejected
        self.buttons.rejected.connect(self.reject)

    # Returns the text from the title and URL input fields.
    def get_input(self):
        return self.title_input.text(), self.url_input.text()
