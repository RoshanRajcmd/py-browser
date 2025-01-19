from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QVBoxLayout
from PyQt5.QtCore import Qt

class BookmarkDialog(QDialog):

    def __init__(self, title, url, parent=None):
        super().__init__(parent)

        # Set up dialog properties
        self.setWindowTitle("Add Bookmark")

        # Create the form layout
        self.form_layout = QFormLayout()

        # Add fields for title and URL
        self.title_input = QLineEdit(self)
        self.url_input = QLineEdit(self)
        self.title_input.setText(title)
        self.url_input.setText(url)
        self.title_input.setStyleSheet("""
            QLineEdit{
            border-radius: 5px;
            padding: 3px;
            background-color: black;
            font-size: 14px;
            color: white;
            }
            QLineEdit:focus{
            border: 2px solid #1E88E5;
            }
        """)
        self.url_input.setStyleSheet("""
            QLineEdit{
            border-radius: 5px;
            padding: 3px;
            background-color: black;
            font-size: 14px;
            color: white;
            }
            QLineEdit:focus{
            border: 2px solid #1E88E5;
            }
        """)
        self.form_layout.addRow("Title:", self.title_input)
        self.form_layout.addRow("URL:", self.url_input)

        # Add standard buttons (OK and Cancel)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        # Connect the OK button to the accept method, which closes the dialog and returns QDialog.Accepted
        self.buttons.accepted.connect(self.accept)
        # Connect the Cancel button to the reject method, which closes the dialog and returns QDialog.Rejected
        self.buttons.rejected.connect(self.reject)

        self.buttons.button(QDialogButtonBox.Ok).setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #6E6E6D;
                padding: 3px;
            }
            QPushButton:hover{
                background-color: #1E88E5;
            }
        """)
        self.buttons.button(QDialogButtonBox.Cancel).setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #6E6E6D;
                padding: 3px;
            }
            QPushButton:hover{
                background-color: #7C7C7B;
            }
        """)

        # Create a vertical layout and add the form layout and button box to it
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.form_layout)
        # Center the buttons in the layout
        self.buttons.setStyleSheet("""
            QDialogButtonBox {
                button-layout: 0;
                qproperty-centerButtons: true;
            }
        """)
        #Centers the buttons inline
        self.layout.setAlignment(self.buttons, Qt.AlignCenter)
        self.layout.addWidget(self.buttons)

        # Set the layout to the dialog
        self.setLayout(self.layout)

        # Adjust the size of the dialog to fit its contents
        self.adjustSize()

    # Returns the text from the title and URL input fields.
    def get_input(self):
        return self.title_input.text(), self.url_input.text()
