from PyQt5.QtWidgets import QLineEdit

class SelectableLineEdit(QLineEdit):

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.selectAll()
