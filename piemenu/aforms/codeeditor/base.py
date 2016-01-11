

from PySide import QtGui

import aforms
from highlighter import Highlighter
from python_highlighting import PythonHighlighter


def createEditor():
    pass


class EditorBase(QtGui.QPlainTextEdit):
    """ EditorBase

    Base editor class.

    """

    # Todo fix up
    # _indentWidth = aforms.config['editor']['tab_size']
    # _indentUsingSpaces = aforms.config['editor']['ident_using_spaces']
    # _showSpaces = aforms.config['editor']['show_whitespace']

    _indentWidth = 4
    _indentUsingSpaces = True
    _showSpaces = True

    def __init__(self, *args, **kwargs):
        super(EditorBase, self).__init__(*args, **kwargs)

        # Make sure editor always has a monospace font.
        self.__zoom = 0
        self.setFont()

        self.__highlighter = Highlighter(self.document())
        self.__highlighter.setRules(PythonHighlighter)

        # Set general document option
        option = self.document().defaultTextOption()
        option.setFlags(option.flags() | option.IncludeTrailingSpaces |
                        option.AddSpaceForLineAndParagraphSeparators)

        if self.indentUsingSpaces():
            option.setFlags(option.flags() | option.ShowTabsAndSpaces)

        self.document().setDefaultTextOption(option)

        # View Settings
        # self.setShowWhitespace()
        # self.setShowLineEndings()
        # self.setWrap()
        # self.setHighlightCurrentLine()
        # self.setLongLineIndicatorPosition()

        # So that graphical elements wont break.
        self.cursorPositionChanged.connect(self.viewport().update)

    def setZoom(self, zoom):
        size = aforms.config['editor']['font_size']
        self.__zoom = int(max(1-size, zoom))
        self.setFont(self.fontInfo().family())
        return self.__zoom

    def setFont(self, font=None):
        """ Set the font for the editor. """

        defaultFont = aforms.font.defaultFont()

        if font is None:
            font = defaultFont

        try:
            font = QtGui.QFont(font)
        except ValueError:
            font = defaultFont
            print('setFont accepts None, QFont or a string')

        font.setStyleHint(font.TypeWriter, font.PreferDefault)
        fontInfo = QtGui.QFontInfo(font)
        family = fontInfo.family() if fontInfo.fixedPitch() else default.family()
        size = defaultFont.pointSize() + self.__zoom

        font = QtGui.QFont(family, size)
        super(EditorBase, self).setFont(font)
        return font

    def indentUsingSpaces(self):
        return self._indentUsingSpaces

    def indentWidth(self):
        return self._indentWidth

    def setIndentWidth(self, value):
        value = int(value)
        if value <= 0:
            raise ValueError('indentWidth must be greater than 0.')
        self._indentWidth = value
        self.setTabStopWidth(self.fontMetric().widtrh('i'*self._indentWidth))

    def indentBlock(self, cursor, amount=1):
        pass
