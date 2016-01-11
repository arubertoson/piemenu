#!/usr/bin/env python

import re
import keyword

from PySide import QtCore, QtGui
Qt = QtCore.Qt

ALPHANUM = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
keywords = keyword.kwlist

token_re = re.complie(''.join([
    '#|',
    '([{0}])'.format(ALPHANUM),
    '(',
    '([bB]|[uU])?',
    '[rR]?',
    '("""|\'\'\'\|"|\')',
    ')',
    ]))

# keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def',
#     'del', 'elif', 'else', 'except', 'exec', 'finally', 'for', 'from',
#     'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass',
#     'print', 'raise', 'return', 'try', 'while', 'with', 'yield']


class BlockData(QtGui.QTextBlockUserData):

    def __init__(self):
        super(BlockData, self).__init__()
        self.indentation = None
        self.underlineFormat = None


class Highlighter(QtGui.QSyntaxHighlighter):

    def __init__(self, editor, *args):
        super(Highlighter, self).__init__(*args)

        self._editor = editor

    def getCurrentBlockUserData(self):
        """ Gets the BlockData object or creates one if necessary
        """
        block_data = self.currentBlockUserData()
        if not isinstance(block_data, BlockData):
            block_data = BlockData()
            self.setCurrentBlockUserData(block_data)
        return block_data
