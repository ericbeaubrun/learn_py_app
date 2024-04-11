from PyQt6.QtWidgets import QPlainTextEdit
from logs.LogsConfig import *


class Console(QPlainTextEdit):
    """
    Cette classe représente la console, elle contient et affiche le texte présent en console.
    """

    CONSOLE_STYLE = "color: #b8b8b8; border: 1px solid #3e3e3e; font-size: 13px;  border: 1px solid #555;"

    CONSOLE_SIMPLE_STYLE = "background-color: #2F3831; " + CONSOLE_STYLE

    CONSOLE_ERROR_STYLE = "background-color: #2A2020; " + CONSOLE_STYLE

    CONSOLE_INVALID_STYLE = "background-color: #2e2e22; " + CONSOLE_STYLE

    def __init__(self):
        super().__init__()
        if FILE_LOGGING:
            logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

        self.setReadOnly(True)
        self.setStyleSheet(self.CONSOLE_SIMPLE_STYLE)
        logging.info("console initialized")

    def set_error_style(self):
        self.setStyleSheet(self.CONSOLE_ERROR_STYLE)

    def set_invalid_style(self):
        self.setStyleSheet(self.CONSOLE_INVALID_STYLE)

    def set_simple_style(self):
        self.setStyleSheet(self.CONSOLE_SIMPLE_STYLE)

    def set_tutorial_text(self, text):
        self.set_simple_style()
        self.clear()
        self.appendPlainText(text)

    def append_text_with_simple_style(self, text):
        self.set_simple_style()
        self.appendPlainText(text)

    def set_text_with_simple_style(self, text):
        self.clear()
        self.append_text_with_simple_style(text)

    def append_text_with_error_style(self, text):
        self.set_error_style()
        self.appendPlainText(text)

    def set_text_with_error_style(self, text):
        self.clear()
        self.append_text_with_error_style(text)

    def append_text_with_invalid_style(self, text):
        self.set_invalid_style()
        self.appendPlainText(text)

    def set_text_with_invalid_style(self, text):
        self.clear()
        self.append_text_with_error_style(text)

    def print_animation_speed(self, animation_speed):
        text = 'Vitesse : '
        match animation_speed:
            case 100:
                text += '⬤ ⬤ ⬤ ⬤ 100%'
            case 300:
                text += '⬤ ⬤ ⬤ ◯ 75%'
            case 500:
                text += '⬤ ⬤ ◯ ◯ 50%'
            case 700:
                text += '⬤ ◯ ◯ ◯ 25%'
            case 900:
                text += '◯ ◯ ◯ ◯ 0%'
        self.appendPlainText(text)
