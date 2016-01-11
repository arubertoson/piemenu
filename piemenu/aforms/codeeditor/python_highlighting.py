""" python_highligher.py

High
"""


import re
import keyword
from tokens import Token


class PythonParser(object):

    def parseLine(self, line, previousState=0):
        pass

    def name(self):
        return self.__class__.__name__.lower()

    def __repr__(self):
        return '<Parser for "{0}"'.format(self.name())


class PythonHighlighter(Token):
    pass


class KeywordToken(PythonHighlighter):
    """ A keyword represents a word with special meaning to the languge. """
    pattern = re.compile(ur'\b({0})\b'.format('|'.join(keyword.kwlist)))
    textFormat = 'color:#CC7833'


class ConstantToken(PythonHighlighter):
    pattern = re.compile(ur'(\b(None|True|False|Ellipsis|NotImplemented)\b)')
    textFormat = 'color:#6D9CBE'


class OperatorToken(PythonHighlighter):
    pattern = re.compile(
        ur'('
        '\=|'  # assignment
        '<\=|>\=|\=\=|<|>|\!\=|'  # comparison
        '\+\=|-\=|\*\=|/\=|//\=|%\=|&\=|\|\=|\^\=|>>\=|<<\=|\*\*\=|'  # inplace
        '\+|\-|\*|\*\*|/|//|%|<<|>>|&|\||\^|~)')  # arithmetic
    textFormat = 'color:#CC7833'


class LanguageVariableToken(PythonHighlighter):
    pattern = re.compile(ur'\b(self|cls)\b')
    textFormat = 'color:#D0D0FF'


class NumberToken(PythonHighlighter):
    pattern = re.compile(ur'(\d)+')
    textFormat = 'color:#a5c261'


class BuiltInTypes(PythonHighlighter):
    pattern = re.compile(
        ur'(?x)\b('
        'basestring|bool|buffer|classmethod|complex|dict|enumerate|file|'
        'float|frozenset|int|list|long|object|open|property|reversed|set|'
        'slice|staticmethod|str|super|tuple|type|unicode|xrange)')
    textFormat = 'color:#6E9CBE'


class ClassNameToken(PythonHighlighter):
    """ Word following class keyword. """
    pattern = re.compile(ur'(?<=\bclass\s)(\b[A-Za-z0-9_]+)(?=\(|\s|$)')
    textFormat = 'color:#FFFFFF'


class FunctionNameToken(PythonHighlighter):
    """ Word Following function keyword. """
    pattern = re.compile(ur'(?<=\bdef\s)(\b[A-Za-z0-9_]+)(?=\(|\s|$)')
    textFormat = 'color:#FFC66D'


class MagicToken(PythonHighlighter):
    pattern = re.compile(
        ur'(?x)\b(__(?:'
        'abs|add|and|call|cmp|coerce|complex|contains|del|delattr|'
        'delete|delitem|delslice|div|divmod|enter|eq|exit|float|'
        'floordiv|ge|get|getattr|getattribute|getitem|getslice|gt|'
        'hash|hex|iadd|iand|idiv|ifloordiv|ilshift|imod|imul|init|'
        'int|invert|ior|ipow|irshift|isub|iter|itruediv|ixor|le|len|'
        'long|lshift|lt|mod|mul|ne|neg|new|nonzero|oct|or|pos|pow|'
        'radd|rand|rdiv|rdivmod|repr|rfloordiv|rlshift|rmod|rmul|ror|'
        'rpow|rrshift|rshift|rsub|rtruediv|rxor|set|setattr|setitem|'
        'setslice|str|sub|truediv|unicode|xor)__)')
    textFormat = 'color:#DA4939'


class BuiltInFunctions(PythonHighlighter):
    pattern = re.compile(
        ur'(?x)\b('
        '__import__|abs|all|any|apply|ascii|bin|bytearray|bytes|callable|'
        'chr|cmp|coerce|compile|delattr|dir|divmod|eval|execfile|filter|'
        'format|getattr|globals|hasattr|hash|help|hex|id|input|intern|'
        'isinstance|issubclass|iter|len|locals|map|max|memoryview|min|'
        'next|oct|ord|pow|range|raw_input|reduce|reload|repr|round|setattr'
        '|sorted|sum|unichr|vars|zip)')
    textFormat = 'color:#DA4939'


class CommentToken(PythonHighlighter):
    """ Character representing a comment in the code. """
    pattern = re.compile(ur'(#.*)')
    textFormat = 'color:#BC9458, italic'


class StringToken(PythonHighlighter):
    pattern = re.compile(ur'("""|\'\'\'|"|\')')
    textFormat = 'color:#a5c261'
    type_ = None


class WhiteSpaceToken(PythonHighlighter):
    pattern = re.compile(ur'(\s)+')
    textFormat = 'color:#585654'
