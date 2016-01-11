# -*- coding: utf-8 -*-
""" behaviour.py

Extensions that handles editors behaviour.

"""

from PySide import QtGui, QtCore
from PySide.QtCore import Qt


class Indentation(object):

    def indentBlock(self, cursor, amount=1):

        text = cursor.block().text()
        leadingWhitespace = text[:len(text)-len(text.lstrip())]

        cursor.movePosition(cursor.StartOfBlock)
        cursor.movePosition(cursor.Right, cursor.KeepAnchor,
                            len(leadingWhitespace))

        indent = len(leadingWhitespace.expandtabs(self.indentWidth()))
        if self.indentUsingSpaces():
            correction = indent % self.indentWidth()
            if correction and amount < 0:
                correction = -(self.indentWidth() - correction)

            indent += (self.indentWidth() * amount) - correction
            cursor.insertText(' ' * max(indent, 0))
        else:
            indent = (indent // self.indentWidth()) + amount
            cursor.insertText('\t' * max(indent, 0))
        self.setTextCursor(cursor)

    def __cursorIsInLeadingWhitespace(self, cursor=None):
        """
        Checks wether the given cursor is in the leading whitespace of a
        block, i.e. before the first non-whitespace character. The cursor
        is not modified. If the cursor is not given or is None, the current
        textCursor is used
        """
        if cursor is None:
            cursor = self.textCursor()

        # Get the text of the current block up to the cursor
        textBeforeCursor = cursor.block().text()[:cursor.positionInBlock()]
        return textBeforeCursor.lstrip() == ''

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()

        cursor = self.textCursor()
        if key == Qt.Key_Tab:
            if modifiers == Qt.NoModifier:
                if self.textCursor().hasSelection():
                    self.indentSelection()
                    return
                elif self.__cursorIsInLeadingWhitespace():
                    self.indentBlock(cursor)
                    return

                elif self.indentUsingSpaces():
                    self.indentBlock(cursor)
                    return
            else:
                return
        elif key == Qt.Key_Backtab:
            self.indentBlock(cursor, -1)
            return


        # If backspace is pressed in the leading whitespace, (except for
        # at the first position of the line), and there is no selection
        # dedent that line and move cursor to end of whitespace
        if (key == Qt.Key_Backspace and modifiers == Qt.NoModifier and
                self.__cursorIsInLeadingWhitespace() and not
                self.textCursor().atBlockStart() and not
                self.textCursor().hasSelection()):
            # Create a cursor, dedent the block and move screen cursor
            # to the end of the whitespace
            cursor = self.textCursor()
            self.indentBlock(cursor, -1)
            self.setTextCursor(cursor)
            return

        # todo: Same for delete, I think not (what to do with the cursor?)

        # Auto-unindent
        if event.key() == Qt.Key_Delete:
            cursor = self.textCursor()
            if not cursor.hasSelection():
                cursor.movePosition(cursor.EndOfBlock, cursor.KeepAnchor)
                if not cursor.hasSelection() and cursor.block().next().isValid():
                    cursor.beginEditBlock()
                    cursor.movePosition(cursor.NextBlock)
                    self.indentBlock(cursor, -99)  # dedent as much as we can
                    cursor.deletePreviousChar()
                    cursor.endEditBlock()
                    return

        super(Indentation, self).keyPressEvent(event)


class AutoIndent(object):

    def keyPressEvent(self,event):

        #This extension code is run *after* key is processed by QPlainTextEdit
        super(AutoIndent, self).keyPressEvent(event)

        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            cursor = self.textCursor()
            previousBlock = cursor.block().previous()
            line = previousBlock.text()
            cursor.beginEditBlock()

            if all([i == ' ' for i in previousBlock.text()]):
                cursor.movePosition(cursor.PreviousBlock)
                cursor.movePosition(cursor.EndOfLine, cursor.KeepAnchor)
                cursor.removeSelectedText()
                cursor.movePosition(cursor.NextBlock)

            if previousBlock.isValid():
                indent = line[:len(line)-len(line.lstrip())]
                if line.endswith(':'):
                    if self.indentUsingSpaces():
                        indent += ' ' * self.indentWidth()
                    else:
                        indent += '\t'
                cursor.insertText(indent)
                cursor.endEditBlock()
            self.setTextCursor(cursor)
