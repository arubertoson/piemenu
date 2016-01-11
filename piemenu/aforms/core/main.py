
""" Module main

Contains the main frame and implements the main window.

"""
import os
import platform

from PySide import QtCore, QtGui

import aforms
from aforms.codeeditor import CodeEditor
from aforms.codeeditor import python_highlighting
# from app import style_rc


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.setMainTitle()
        # self.setWindowIcon()

        self.resize(800, 600)
        # self.restoreGeometry()

        window_icon = aforms.icon['window']
        self.setWindowIcon(window_icon)

        self.show()

        self._populate()


    def _populate(self):
        from aforms.core.fields import TextField

        widget = CodeEditor()
        self.setCentralWidget(widget)
        # widget = QtGui.QLabel('Hello darr!')
        # widget = QtGui.QPushButton('Yay')
        # t = QtGui.QIcon(':icons/toolbar_command.png')
        # widget.setIcon(t)
        # widget.setPixmap(t)
        # self.setCentralWidget(widget)

        # self._shellDock = dock = QtGui.QDockWidget(self)
        # dock.setObjectName('shells')
        # dock.setWindowTitle('Shells')
        # self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock)

    def setMainTitle(self):
        title = 'Command System'
        self.setWindowTitle(title)

    def closeEvent(self, event):
        # implement save config
        QtGui.QMainWindow.closeEvent(self, event)


