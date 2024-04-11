from PyQt6.Qsci import QsciLexerPython, QsciScintilla
from PyQt6.QtGui import QColor


class EditorLexer(QsciLexerPython):
    """
    Cette classe permet de définir la coloration elxicale de l'editor de code.
    """

    def __init__(self):
        super().__init__()
        self.setDefaultPaper(QColor("#2b2b2b"))
        self.setColor(QColor("#f8f8f2"))
        self.setColor(QColor("#f92672"), QsciLexerPython.Keyword)
        self.setColor(QColor("#e6db74"), QsciLexerPython.Number)
        # lexer.setColor(QColor("#66d9ef"), QsciLexerPython.Comment)
        self.setColor(QColor("#8d8f8b"), QsciLexerPython.Comment)
        self.setColor(QColor("#e6db74"), QsciLexerPython.Operator)
        self.setColor(QColor("#f92672"), QsciLexerPython.ClassName)
        self.setColor(QColor("#a6e22e"), QsciLexerPython.Decorator)
        self.setColor(QColor("#ffffff"), QsciLexerPython.Decorator)
        self.setColor(QColor("#f8f8f2"), QsciLexerPython.UnclosedString)
        self.setColor(QColor("#a6e22e"), QsciLexerPython.DoubleQuotedString)
        self.setColor(QColor("#f92672"), QsciLexerPython.FunctionMethodName)
        self.setColor(QColor("#a6e22e"), QsciLexerPython.SingleQuotedString)
        self.setColor(QColor("#f92672"), QsciLexerPython.HighlightedIdentifier)
