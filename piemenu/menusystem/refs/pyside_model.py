# usr/bin/env python2

from PySide import QtCore, QtGui
from PySide.QtCore import Qt







class QPieMenuModel(QtCore.QAbstractItemModel):


    def __init__(self):
        super(QPieMenuModel, self).__init__(self)

    # row=int, column=int, parent=QtCore.QModelIndex
    def index(self, row, column, parent):
        pass

    # Takes child=QtCore.QModelIndex
    def parent(self, child):
        pass

    # Takes parent=QtCore.QModelIndex
    def hasChildren(self, parent):
        pass

    # Takes parent=QtCore.QModelIndex
    def rowCount(self, parent):
        pass

    # Takes parent=QtCore.QModelIndex
    def columnCount(self, parent):
        pass

    # Takes index=QtCore.QModelIndex, role=Qt.Displayrole
    def data(self, index, role):
        pass

    # Takes index=QtCore.QModelIndex, value=object, role=QtDisplayRole
    def setData(self, index, value, role):
        pass

    # takes section=int. orientation=Qt.Orientation, role=Qt.DisplayRole
    def headerData(self, section, orientation, role):
        pass

    # Takes index=QtModelIndex
    def flags(index):
        pass


        pass
