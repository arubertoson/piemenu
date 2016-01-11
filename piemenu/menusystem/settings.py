from PySide import QtCore, QtGui
import resource_rc


class Icon:
    TextOnly, IconOnly, TextAndIcon, SmallIcons, BigIcons = range(5)

    SmallSize = QtCore.QSize(16, 16)
    BigSize = QtCore.QSize(32, 32)

    Command = ':command.png'
    AddCommand = ':addcommand.png'
    Form = ':form.png'
    AddForm = ':addform.png'
    Separator = ':separator.png'
    AddSeparator = ':addseparator.png'
    Settings = ':settings.png'
    Delete = ':delete.png'
    Search = ':search.png'
    MoveUp = ':moveup.png'
    MoveDown = ':movedown.png'


class Font:

    EditorFont = QtGui.QFont()
    EditorFont.setFamily('Source Code Pro')
    EditorFont.setStyleHint(QtGui.QFont.Monospace)
    EditorFont.setPointSize(9)
    EditorFont.setFixedPitch(True)

    AppFont = QtGui.QFont()
    AppFont.setFamily('Tahoma')
    AppFont.setStyleHint(QtGui.QFont.Monospace)
    AppFont.setPointSize(10)
    AppFont.setFixedPitch(True)
