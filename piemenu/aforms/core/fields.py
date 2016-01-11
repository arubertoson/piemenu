
from PySide import QtCore, QtGui
Qt = QtCore.Qt

import aforms


class TextField(QtGui.QLineEdit):

    def __init__(self, icon=aforms.icon['search'], parent=None):
        super(TextField, self).__init__(parent)

        self.setMinimumHeight(40)
        self.setTextMargins(36, 0, 0, 0)
        self.setPlaceholderText('Search ...')
        self.button = self.initIcon(icon)

        self.setFont(aforms.font.default_font())

    def initIcon(self, icon):
        button = QtGui.QToolButton(self)
        button.setIcon(QtGui.QIcon(icon))
        button.setIconSize(QtCore.QSize(20, 20))
        button.setEnabled(False)
        button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        return button

    def resizeEvent(self, event):
        super(TextField, self).resizeEvent(event)
        self.layoutButton()

    def layoutButton(self):
        self.ensurePolished()

        w, h = self.button.minimumSizeHint().toTuple()
        point = QtCore.QPoint(w/1.75, self.rect().height()/2)

        rect = QtCore.QRect(0, 0, w, h)
        rect.moveCenter(point)
        self.button.setGeometry(rect)
        self.setTextMargins(*self.getTextMargins())
