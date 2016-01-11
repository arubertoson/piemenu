#! usr/bin/env python2

from PySide import QtGui, QtCore
from PySide.QtCore import Qt


from settings import Icon


class Node(object):

    Command, Form, Separator = 'command', 'form', 'separator'

    @classmethod
    def from_type(cls, type_, **kw):
        cls = Command if kw['type'] == cls.Command else Form
        return cls(**kw)

    def __init__(self, **kw):

        self._parent = kw.get('parent', None)
        self._type = kw.get('type', None)
        self._style = kw.get('style', None)

        self._label = kw.get('label', '')
        self._description = kw.get('description', '')
        self._items = kw.get('items', [])

        self._qactive = True
        self.setParent(self._parent)

    @property
    def qactive(self):
        return self._qactive

    @qactive.setter
    def qactive(self, value):
        self._qactive = value

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.label())

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

    def style(self):
        return self._style

    def parent(self):
        return self._parent

    def items(self):
        return self._items

    def setData(self, column, value):
        if not column == 0:
            return False
        self._label = value
        return True

    def setParent(self, parent):
        if parent is not None:
            self._parent = parent
            self._parent.appendItem(self)
        else:
            self._parent = None

    def getItem(self, row):
        if len(self._items) > row:
            return self._items[row]

    def getItemAtRow(self, child):
        for i, item in enumerate(self._items):
            if item == child:
                return i
        return -1

    def appendItem(self, node):
        self._items.append(node)

    def insertItem(self, row, node):
        if row < 0 or row > len(self.items()):
            return False
        self._items.insert(row, node)
        node._parent = self
        return True

    def removeItem(self, row):
        item = self._items.pop(row)
        item._parent = None
        return True

    def columnCount(self):
        return len(self._headers)

    def row(self):
        if self._parent is not None:
            return self._parent._items.index(self)
        return -1

    def sizeHint(self):
        return QtCore.QSize(16, 16)

    def log(self, level=-1):
        level += 1
        output = ['\t' for i in range(level)]
        output.append(self._label if self._parent is not None else 'Root')
        output.append('\n')
        output.extend([item.log(level) for item in self._items])
        level -= 1
        return ''.join(output)


class Command(Node):

    def __init__(self, **kw):
        super(Command, self).__init__(**kw)

        self._type = Node.Command
        self._icon = kw.get('icon', '')
        self._command = kw.get('command', '')
        self._sub_command = kw.get('sub_command', '')
        self._label = 'Untitled Command' if self._label == '' else self._label

    def icon(self):
        return self._icon

    def command(self):
        return self._command

    def subCommand(self):
        return self._sub_command


class Form(Node):

    def __init__(self, **kw):
        super(Form, self).__init__(**kw)

        self._type = Node.Form
        self._icon_mode = kw.get('icon_mode', 0)
        self._icon_size = kw.get('icon_size', 4)
        self._label = 'Untitled Form' if self._label == '' else self._label

    def iconMode(self):
        return self._icon_mode

    def iconSize(self):
        return self._icon_size


class Separator(Node):

    def __init__(self, **kw):
        super(Separator, self).__init__(**kw)

        self._type = Node.Separator
        self._label = 'separator'
