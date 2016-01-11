
import sys
import cPickle


from PySide import QtGui, QtCore
from PySide.QtCore import Qt


class Node(object):

    def __init__(self, parent=None):

        self._parent = parent
        self._label = 'root'
        self._type = None
        self._items = []

        self.setParent(parent)

    def __repr__(self):
        return self.log()

    def __len__(self):
        return len(self._items)

    def label(self):
        return self._label

    def type(self):
        return self._type

    def parent(self):
        return self._parent

    def setParent(self, parent):
        if parent is not None:
            self._parent = parent
            self._parent.appendItem(self)
        else:
            self._parent = None

    def getItem(self, row):
        return self._items[row]

    def appendItem(self, node):
        self._items.append(node)

    def appendChild(self, node):
        self._items.append(node)

    def insertItem(self, row, node):
        self._items.insert(row, node)

    def removeItem(self, row):
        item = self._items[row]
        self._items.remove(item)

    def columnCount(self):
        return 2

    def row(self):
        if self._parent is not None:
            return self._parent._items.index(self)
        return -1

    def log(self, level=-1):
        level += 1
        output = ['\t' for i in range(level)]
        output.append(self._label if self._parent is not None else 'Root')
        output.append('\n')
        output.extend([item.log(level) for item in self._items])
        level -= 1
        return ''.join(output)




if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    rootNode = Node()
    childnode0 = Node(rootNode)
    childnode0._label = 'Something'

    childnode1 = Node(childnode0)
    childnode1._label = 'Left Foot'

    childnode2 = Node(rootNode)
    childnode2._label = 'Testy'

    print rootNode

    model = SceneGraph(rootNode)

    tree = QtGui.QTreeView()

    tree.setDragEnabled(True)
    tree.setAcceptDrops(True)
    tree.setDropIndicatorShown(True)
    tree.setDragDropMode(QtGui.QAbstractItemView.InternalMove)

    # tree.change.connect()

    tree.setModel(model)
    tree.show()

    sys.exit(app.exec_())
