#!/usr/bin/env python

import re

from PySide import QtCore, QtGui
Qt = QtCore.Qt


#TODO Move
str_literals = ['', "'''", '"""', "'", '"']
str_token_end = {
    "'": re.compile(r"(^|[^\\])(\\\\)*'"),
    '"': re.compile(r'(^|[^\\])(\\\\)*"'),
    "'''": re.compile(r"(^|[^\\])(\\\\)*'''"),
    '"""': re.compile(r'(^|[^\\])(\\\\)*"""'),
    }


class Highlighter(QtGui.QSyntaxHighlighter):

    endstate = False

    def __init__(self, editor, *args):
        super(Highlighter, self).__init__(editor, *args)
        self._editor = editor
        self._rules = None

    def _getStringToken(self):
        for token in self._rules:
            class_name = token.__class__.__name__
            if class_name == 'StringToken':
                return class_name

    def setRules(self, baseclass):
        try:
            self._rules = baseclass.__subclasses__()
        except:
            pass

    def highlightBlock(self, line):

        # print self.currentBlock().blockNumber()

        previousState = self.previousBlockState()
        self.setCurrentBlockState(0)

        print 'previous state: ' + str(previousState)
        for token in self._rules:
            pos = 0
            state = 0

            if previousState in [1, 2, 3, 4]:
                strtoken = token(0)
                if not strtoken.name == 'StringToken':
                    continue
                strtoken.type_ = str_literals[previousState]
                strtoken, state = self._findEndOfString(line, strtoken)
                self.setFormat(strtoken.start,
                               strtoken.lenght,
                               strtoken.textCharFormat)
                print 'state after stringblock: ' + str(state)
                if state in [1, 2, 3, 4]:
                    self.setCurrentBlockState(state)
                    return
                pos = strtoken.end

            while pos >= 0:

                nexttoken = self._findNextToken(token, line, pos)
                if nexttoken is None:
                    break
                elif nexttoken.name == 'StringToken':
                    nexttoken, state = self._findEndOfString(line, nexttoken)
                print 'state before stringblock: ' + str(state)
                self.setCurrentBlockState(state)
                self.setFormat(nexttoken.start,
                               nexttoken.lenght,
                               nexttoken.textCharFormat)
                if state in [1, 2, 3, 4]:
                    return
                pos = nexttoken.end

    def _findEndOfString(self, line, token):
        """ Find the end of a string. Returns (token, state). """
        style = token.type_
        endmatch = str_token_end[style].search(line[token.end:])

        print endmatch, style
        if endmatch:
            start, end = token.start, token.end + endmatch.end()
            state = 0
        else:
            start, end = token.start, token.end + len(line)
            state = str_literals.index(style)

        token.start, token.end = start, end
        return token, state

    def _findNextToken(self, token, line, pos):
        """ Returns a matching token or None if no token can be found. """
        if pos >= len(line):
            return None

        token_type = token(pos)
        match = token_type.search(line)
        if match is None:
            return

        if token_type.name == 'StringToken':
            token_type.type_ = match.group()
        token_type.start, token_type.end = match.start(), match.end()
        return token_type
