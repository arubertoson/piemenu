""" Module tokens

Defines python specific tokens. Tokens are used by the parsers to identify
what they represent. This is used by highlighter to determine how these
characters should be represented.

"""

import re
import keyword
from PySide import QtGui


class BlockState(object):
    """
    The blockstate object should be used by parsers to
    return the block state of the processed line.
    """
    isToken = False

    def __init__(self, state=0, info=None):
        self._state = int(state)
        self._info = info

    @property
    def state(self):
        """ The integer value representing the block state.
        """
        return self._state

    @property
    def info(self):
        """ Get the information corresponding to the block.
        """
        return self._info


class Token(object):
    """ Token()

    Base token class.

    A token is a group of characters found by the specified regex pattern.

    """
    pattern = re.compile(ur'')
    textFormat = 'color:#000, bold:no, italic:no'

    def __new__(cls, *args, **kwargs):
        return cls._from_parts(*args, **kwargs)

    @classmethod
    def _from_parts(cls, start, end=0):
        self = object.__new__(cls)
        self.start, self.end = start, end
        self._parts = {}
        self.update()
        return self

    def __repr__(self):
        return '<Token "{0}"'.format(self.__class__.__name__)

    def _initProperties(self):
        self._color = None
        self._bold = None
        self._italic = None
        self._textCharFormat = None

    def update(self):
        """ update()

        Updates format style with given textFormat.

        """
        self._initProperties()
        styleParts = [
            p for p in self.textFormat \
            .replace('=', ':') \
            .replace(';', ',')
            .split(',') \
            ]

        for part in styleParts:
            if ':' not in part:
                if part.startswith('#'):
                    part = 'color:{0}'.format(part)
                else:
                    part += ':yes'

            key, _, val = [_.strip().lower() for _ in part.partition(':')]
            self._parts[key] = val

    def search(self, line):
        line = unicode(line)
        match = self.pattern.search(line, self.start)
        if match is None:
            return
        return match

    def _getValue(self, key):
        try:
            return self._parts[key]
        except KeyError:
            return False

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def textCharFormat(self):
        if self._textCharFormat is None:
            textCharFormat = QtGui.QTextCharFormat()
            textCharFormat.setForeground(self.color)
            if self.bold:
                textCharFormat.setFontWeight(QtGui.QFont.Bold)
            if self.italic:
                textCharFormat.setFontItalic(True)
            self._textCharFormat = textCharFormat
        return self._textCharFormat

    @property
    def lenght(self):
        """ The character lenght of the current matching group. """
        return self.end - self.start

    @property
    def bold(self):
        if self._bold is None:
            self._bold = True if self._getValue('bold') else False
        return self._bold

    @property
    def italic(self):
        if self._italic is None:
            self._italic = True if self._getValue('bold') else False
        return self._italic

    @property
    def color(self):
        if self._color is None:
            self._color = QtGui.QColor(self._parts['color'])
        return self._color


