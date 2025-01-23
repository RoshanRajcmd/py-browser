from PyQt5.QtWidgets import QDialog, QVBoxLayout
from BookmarkBar import BookmarkBar

class ShowBookmarksDialog(QDialog):
    def __init__(self, mainWindow, parent=None):
        super().__init__(parent)
        self.mainWindow = mainWindow
        self.parent = parent


        self.setWindowTitle("Bookmarks")
        layout = QVBoxLayout()

        for bookmark in self.mainWindow.bookmarks:
            bookmark_bar = BookmarkBar(self.mainWindow, bookmark['title'], bookmark['url'], self)
            layout.addWidget(bookmark_bar)

        self.setLayout(layout)
        self.adjustSize()

    def save_bookmark(self):
        self.parent.save_bookmark()
        self.parent.render_show_bookmarks_dialog()

    def delete_bookmark(self, url):
        self.parent.delete_bookmark(url)