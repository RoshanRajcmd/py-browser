from PyQt5.QtWidgets import QLineEdit

class SelectableLineEdit(QLineEdit):
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.selectAll()
