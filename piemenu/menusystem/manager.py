#! python2
"""
"""
from PySide import QtCore, QtGui
from PySide.QtCore import Qt

import json
from json_minify import json_minify
from path import Path

import cPickle as pickle
from cStringIO import StringIO

from node import Node, Command, Form, Separator
from settings import Icon

PIE_EXT = '.piemenu'
CWD = Path(__file__).dirname().expand()
CONFIG_PATHS = [CWD, Path(CWD.parent).joinpath('config')]


class PieManager(object):

    command_key, form_key = 'commands', 'forms'
    commands, forms = {}, {}

    def __init__(self):
        self.config_files = self.get_config_files()

    def get_config_files(self, paths=CONFIG_PATHS):
        config_files = {}
        for p in paths:
            if not p.exists():
                continue
            for f in p.files():
                if not f.ext == PIE_EXT:
                    continue
                config_files[f.namebase] = f
        return config_files

    def get_json_data(self, input_file):
        with open(str(input_file), 'r') as f:
            json_string = json_minify(''.join(f.readlines()))
            json_data = json.loads(json_string)
        return json_data

    def process_config(self, file_):
        json_data = self.get_json_data(file_)

        for command in json_data[self.command_key]:
            self.commands[command['label']] = command

        for form in json_data[self.form_key]:
            type_ = form['type']
            node = Node.from_type(type_, **form)
            self.forms[node.label()] = node

        for form in self.forms.values():
            items = []
            for item in form._items[:]:
                try:
                    item = self.commands[item]
                    type_ = item['type']
                    node = Node.from_type(type_, **item)
                except:
                    node = self.forms[item]
                node.setParent(form)
                items.append(node)
            form._items = items

    def delete_command(self, command):
        del self.command[command]

    def delete_form(self, form):
        del self.forms[form]

    def update(self):
        self.commands.clear()
        self.forms.clear()
        self.config_files = self.get_config_files(CONFIG_PATHS)
        self.process_config()


class FormItemModel(QtCore.QAbstractItemModel):

    headers = ['Label', 'Description']

    def __init__(self, root, parent=None):
        super(FormItemModel, self).__init__(parent)

        self._root = root

    def root(self):
        return self._root

    def nodeFromIndex(self, index):
        return index.internalPointer() if index.isValid() else self._root

    def unpickleIndices(self, data):
        nodes = []
        stream = StringIO(str(data.data('application/x-menus')))
        while True:
            try:
                nodes.append(pickle.load(stream))
            except EOFError:
                break
        return nodes

    def pickleIndices(self, indices):
        nodes = []
        stream = StringIO()
        for index in indices:
            if not index.isValid():
                continue

            node = self.nodeFromIndex(index)
            if node in nodes:
                continue
            nodes.append(node)
            pickle.dump(node, stream)
            stream.flush()
        serialized_data = stream.getvalue()
        stream.close()
        return serialized_data

    def index(self, row, column, parent):
        parent_item = self.nodeFromIndex(parent)
        return self.createIndex(row, column, parent_item.getItem(row))

    def parent(self, index):
        node = self.nodeFromIndex(index)

        if node is None:
            return QtCore.QModelIndex()

        parent = node.parent()
        if parent == self._root or parent is None:
            return QtCore.QModelIndex()

        grandparent = parent.parent()
        if grandparent is None:
            return QtCore.QModelIndex()

        row = grandparent.getItemAtRow(parent)
        assert row != -1

        return self.createIndex(row, 0, parent)

    def rowCount(self, index):
        return len(self.nodeFromIndex(index))

    def columnCount(self, index):
        return 1
        # return len(self.headers)

    def data(self, index, role):

        if not index.isValid():
            return None

        node = index.internalPointer()
        if role in [Qt.EditRole, Qt.DisplayRole]:
            return node._label

        if role == Qt.DecorationRole and index.column() == 0:

            type_ = node.type()
            if type_ == Node.Command:
                return QtGui.QIcon(Icon.Command)
            elif type_ == Node.Form:
                return QtGui.QIcon(Icon.Form)
            elif type_ == Node.Separator:
                return QtGui.QIcon(Icon.Separator)

    def setData(self, index, value, role):
        if not role == Qt.EditRole:
            return False

        node = self.nodeFromIndex(index)
        result = node.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)
        return result

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]

    def supportedDropActions(sefl):
        return Qt.MoveAction

    def flags(self, index):
        flags = QtCore.QAbstractItemModel.flags(self, index)

        if not index.isValid():
            return QtCore.Qt.ItemIsDropEnabled | flags

        node = self.nodeFromIndex(index)
        if node is None:
            return flags
        elif node.type() == Node.Command:
            return Qt.ItemIsDragEnabled | Qt.ItemIsEditable | flags
        return Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEditable | flags

    def mimeTypes(self):
        return ['application/x-menus']

    def mimeData(self, indices):
        mimedata = QtCore.QMimeData()
        mimedata.setData('application/x-menus', self.pickleIndices(indices))
        return mimedata

    def dropMimeData(self, data, action, row, column, index):
        if not row == -1:
            pass
        elif index.isValid():
            row = 0
        else:
            row = self.rowCount(QtCore.QModelIndex())
        nodes = self.unpickleIndices(data)
        self.insertRows(row, nodes, index)
        return True

    def removeRows(self, row, count, index):
        self.beginRemoveRows(index, row, (row + (count-1)))

        parent = self.nodeFromIndex(index)
        for x in xrange(count):
            parent.removeItem(row)
        self.endRemoveRows()
        return True

    def insertRows(self, row, nodes, index, node_type=None):
        parent = self.nodeFromIndex(index)
        self.beginInsertRows(index, row, row+(len(nodes)-1))
        for dropped_node in nodes:
            if node_type is not None:
                dropped_node = {
                    Node.Command: Command(),
                    Node.Form: Form(),
                    Node.Separator: Separator(),
                }[node_type]
            parent.insertItem(row, dropped_node)

        self.endInsertRows()
        self.dataChanged.emit(parent, parent)
        return True
