

from PySide import QtGui

import aforms
# from .highlighter import Highlighter


class EditorBase(QtGui.QPlainTextEdit):
    """ EditorBase

    Base editor class.

    """

    def __init__(self, *args, **kwargs):
        super(EditorBase, self).__init__(*args, **kwargs)

        self.setFont(aforms.config['editor']['font_family'])



class Editor(QtGui.QPlainTextEdit):

    tabstop = 4

    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)

        self.setFont(Font.EditorFont)

        metrics = QtGui.QFontMetrics(self.font())
        self.setTabStopWidth(self.tabstop * metrics.width(' '))

        option = self.document().defaultTextOption()
        option.setFlags(option.flags() | option.ShowTabsAndSpaces |
                        option.IncludeTrailingSpaces |
                        option.AddSpaceForLineAndParagraphSeparators)
        self.document().setDefaultTextOption(option)

        self.__highlighter = Highlighter(self, self.document())
        self.cursorPositionChanged.connect(self.viewport().update)

    def keyPressEvent(self, event):
        key = event.key()
        key_mod = event.modifiers()
        cursor = self.textCursor()
        front_char = cursor.block().text()[:cursor.positionInBlock()].lstrip()

        if key == Qt.Key_Tab:
            if key_mod == Qt.NoModifier:
                self.indentBlock(cursor)
                return
            elif front_char == '':
                self.indentBlock(cursor)
                self.setTextCursor(cursor)
                return
        elif key == Qt.Key_Backtab:
            self.indentBlock(cursor, -1)
            return

        if (key == Qt.Key_Backspace and key_mod == Qt.NoModifier and
                front_char == '' and not cursor.atBlockStart() and not
                cursor.hasSelection()):
            self.indentBlock(cursor, -1)
            return
        super(Editor, self).keyPressEvent(event)

    def indentBlock(self, cursor, direction=1):
        text = cursor.block().text()
        leadingWhitespace = text[:len(text)-len(text.lstrip())]

        cursor.movePosition(cursor.StartOfBlock)
        cursor.movePosition(cursor.Right, cursor.KeepAnchor,
                            len(leadingWhitespace))

        indent = len(leadingWhitespace.expandtabs(self.tabstop))
        correction = indent % self.tabstop
        if correction and direction < 0:
            correction = -(self.tabstop - correction)

        indent += (self.tabstop * direction) - correction
        cursor.insertText(' '*max(indent, 0))

