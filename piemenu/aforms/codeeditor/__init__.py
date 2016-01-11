
from base import EditorBase
from behaviour import Indentation, AutoIndent


class CodeEditor(Indentation,
                 AutoIndent,
                 EditorBase,
                 ):
    pass
