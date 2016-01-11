#! usr/bin/env python2

from PySide import QtGui, QtCore
from PySide.QtCore import Qt


class Icon:
    TextOnly, IconOnly, TextAndIcon, SmallIcons, BigIcons = range(5)

    qSmallSize = QtCore.QSize(16, 16)
    qBigSize = QtCore.QSize(32, 32)


class Node(object):

    @classmethod
    def from_type(cls, type_, **kw):
        type_, style = type_.split('/')
        cls = Command if type_ == 'command' else Form
        return cls(style, **kw)

    def __init__(self, style, **kw):

        self._parent = kw.get('parent', 'root')
        self._type = style

        self._label = kw.get('label', '')
        self._description = kw.get('description', '')
        self._items = kw.get('items', [])
        self.setParent(self._parent)

    def __repr__(self):
        return self.log()

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items

    def label(self):
        return self._label

    def description(self):
        return self._description

    def type(self):
        return self._type

    def parent(self):
        return self._parent

    def items(self):
        return self._items

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
        return 1

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


class Command(Node):

    def __init__(self, style, **kw):
        super(Command, self).__init__(style, **kw)

        self._icon = kw.get('icon', '')
        self._command = kw.get('command', '')
        self._sub_command = kw.get('sub_command', '')

    def icon(self):
        return self._icon

    def command(self):
        return self._command

    def subCommand(self):
        return self._sub_command


class Form(Node):

    def __init__(self, style, **kw):
        super(Form, self).__init__(style, **kw)

        self._icon_mode = kw.get('icon_mode', 0)
        self._icon_size = kw.get('icon_size', 4)

    def iconMode(self):
        return self._icon_mode

    def iconSize(self):
        return self._icon_size
