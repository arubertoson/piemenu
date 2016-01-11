#! python2
"""
"""
from PySide import QtCore, QtGui
from PySide.QtCore import Qt

from manager import PieManager, FormItemModel
from node import Node
from settings import Icon, Font
import resource_rc
import qdarkstyle
from qdarkstyle import compile_qrc

# from highlighter import Highlighter

from editor import Editor



class LineEdit(QtGui.QLineEdit):

    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)
        self.setMinimumHeight(40)
        self.setTextMargins(36, 0, 0, 0)
        self.button = self.searchButton()
        self.setPlaceholderText('Search ...')

        self.setFont(Font.EditorFont)

    def searchButton(self):
        button = QtGui.QToolButton(self)
        button.setIcon(QtGui.QIcon(Icon.Search))
        button.setIconSize(QtCore.QSize(20, 20))
        button.setEnabled(False)
        button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        return button

    def resizeEvent(self, event):
        super(LineEdit, self).resizeEvent(event)
        self.layoutButton()

    def layoutButton(self):
        self.ensurePolished()

        w, h = self.button.minimumSizeHint().toTuple()
        point = QtCore.QPoint(w/1.75, self.rect().height()/2)

        rect = QtCore.QRect(0, 0, w, h)
        rect.moveCenter(point)
        self.button.setGeometry(rect)
        self.setTextMargins(*self.getTextMargins())


class MainWindow(QtGui.QWidget):

    def __init__(self, model):
        super(MainWindow, self).__init__()

        self.resize(900, 600)
        self.initUI()

        self.setFocusPolicy(Qt.ClickFocus)
        self.setFont(Font.EditorFont)

    def initView(self, model):
        view = QtGui.QTreeView(self)
        view.setModel(model)
        view_selection = view.selectionModel()

        # Context
        view.setContextMenuPolicy(Qt.CustomContextMenu)
        view.customContextMenuRequested.connect(self.showContextMenu)

        # View attributes
        view.setEditTriggers(view.EditKeyPressed)
        view.setAcceptDrops(True)
        view.setDragEnabled(True)
        view.setAutoExpandDelay(300)
        view.setDropIndicatorShown(True)
        # view.setAlternatingRowColors(True)
        view.setExpandsOnDoubleClick(True)
        view.setSelectionMode(view.ExtendedSelection)
        view.setSelectionBehavior(view.SelectRows)

        view.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        view.setAttribute(Qt.WA_MacShowFocusRect, True)

        # Header
        view.header().setVisible(False)
        view.header().setResizeMode(view.header().Fixed)
        view.header().resizeSection(0, 280)
        view.header().setMovable(False)
        view.header().setStretchLastSection(True)

        return view, view_selection

    def initContext(self):
        menu = QtGui.QMenu(self)

        newform = QtGui.QAction('Add New &Form...', menu)
        newform.setIcon(QtGui.QIcon(Icon.AddForm))
        newform.triggered.connect(self.insertForm)

        newcommand = QtGui.QAction('Add New &Command...', menu)
        newcommand.setIcon(QtGui.QIcon(Icon.AddCommand))
        newcommand.triggered.connect(self.insertCommand)

        newseparator = QtGui.QAction('Add New &Separator...', menu)
        newseparator.setIcon(QtGui.QIcon(Icon.AddSeparator))
        newseparator.triggered.connect(self.insertSeparator)

        delete = QtGui.QAction('&Delete', menu)
        delete.setIcon(QtGui.QIcon(Icon.Delete))
        delete.triggered.connect(self.deleteNode)

        menu.addAction(newform)
        menu.addAction(newcommand)
        menu.addAction(newseparator)
        menu.addSeparator()
        menu.addAction(delete)
        return menu

    def initToolbar(self):
        toolbar = QtGui.QToolBar(self)
        toolbar.setObjectName('toolbar')
        toolbar.setOrientation(Qt.Horizontal)
        toolbar.setContentsMargins(0, 0, 0, 0)

        #TODO: Add save, load, update, close
        settings_menu = QtGui.QMenu(toolbar)
        settings_menu.addAction('testy1')
        settings_menu.addAction('testy2')

        settings = QtGui.QToolButton(toolbar)
        settings.setIcon(QtGui.QIcon(Icon.Settings))
        settings.setPopupMode(settings.InstantPopup)
        settings.setShortcut('Ctrl+s')
        settings.setMenu(settings_menu)

        moveup = QtGui.QAction('Move Item Up', toolbar)
        moveup.setIcon(QtGui.QIcon(Icon.MoveUp))
        moveup.setShortcut('Ctrl+Up')
        moveup.triggered.connect(self.moveUp)

        movedown = QtGui.QAction('Move Item Down', toolbar)
        movedown.setIcon(QtGui.QIcon(Icon.MoveDown))
        movedown.setShortcut('Ctrl+Down')
        movedown.triggered.connect(self.moveDown)

        addform = QtGui.QAction('Add New Form...', toolbar)
        addform.setIcon(QtGui.QIcon(Icon.AddForm))
        addform.setShortcut('Ctrl+N')
        addform.triggered.connect(self.insertForm)

        addcommand = QtGui.QAction('Add New Command...', toolbar)
        addcommand.setIcon(QtGui.QIcon(Icon.AddCommand))
        addcommand.setShortcut('Ctrl+Shift+N')
        addcommand.triggered.connect(self.insertCommand)

        addseparator = QtGui.QAction('Add New Separator...', toolbar)
        addseparator.setIcon(QtGui.QIcon(Icon.AddSeparator))
        addseparator.setShortcut('Ctrl+Shift+Alt+N')
        addseparator.triggered.connect(self.insertSeparator)

        delete = QtGui.QAction('Delete Selected...', toolbar)
        delete.setIcon(QtGui.QIcon(Icon.Delete))
        delete.setShortcut('Del')
        delete.triggered.connect(self.deleteNode)

        toolbar.addWidget(settings)
        toolbar.addAction(moveup)
        toolbar.addAction(movedown)
        toolbar.addAction(addform)
        toolbar.addAction(addcommand)
        toolbar.addAction(addseparator)
        toolbar.addAction(delete)
        return toolbar

    def initUI(self):
        self.layout = QtGui.QHBoxLayout(self)

        self.menuLayout = QtGui.QVBoxLayout(self)
        self.detailLayout = QtGui.QVBoxLayout(self)

        self.menuLayout.setContentsMargins(8, 8, 8, 8)

        self.model = model
        self.view, self.view_selection = self.initView(model)
        self.viewcontext = self.initContext()
        self.viewsearch = LineEdit(self)
        self.viewtoolbar = self.initToolbar()

        self.editor = Editor(self)

        self.detailLayout.addWidget(self.editor)
        self.menuLayout.addWidget(self.viewtoolbar)
        self.menuLayout.addWidget(self.viewsearch)
        self.menuLayout.addWidget(self.view)

        self.layout.addLayout(self.menuLayout)
        self.layout.addLayout(self.detailLayout)
        self.layout.setStretchFactor(self.menuLayout, 2)
        self.layout.setStretchFactor(self.detailLayout, 3)

        self.setStyleSheet()
        self.setLayout(self.layout)

    def setStyleSheet(self):
        compile_qrc.compile_all()
        stylesheet = qdarkstyle.load_stylesheet()
        super(MainWindow, self).setStyleSheet(stylesheet)

    def showContextMenu(self):
        point = QtGui.QCursor.pos()
        self.viewcontext.exec_(point)

    def insertIndex(self, type_):
        index = self.view_selection.currentIndex()
        node = index.internalPointer()
        isForm = node.type() == Node.Form

        parent = index if isForm else index.parent()
        row = 0 if isForm else index.row()+1

        self.model.insertRows(row, [index], parent, type_)
        new_node = self.model.index(row, 0, parent)

        self.view.clearSelection()
        self.view.setCurrentIndex(new_node)
        self.view.edit(new_node)

    def insertForm(self):
        self.insertIndex(Node.Form)

    def insertCommand(self):
        self.insertIndex(Node.Command)

    def insertSeparator(self):
        self.insertIndex(Node.Separator)

    def deleteNode(self):
        index = self.view_selection.currentIndex()
        self.model.removeRows(index.row(), 1, index.parent())

    def moveUp(self):
        print 'up'

    def moveDown(self):
        print 'down'


if __name__ == '__main__':
    import sys

    m = PieManager()
    m.process_config(m.config_files['template'])

    app = QtGui.QApplication(sys.argv)

    root_item = Node()

    for form in m.forms.values():
        if form.parent() is None:
            form.setParent(root_item)

    print root_item.log()
    model = FormItemModel(root_item)
    window = MainWindow(model)

    # window = TestWindow()

    window.show()
    sys.exit(app.exec_())
