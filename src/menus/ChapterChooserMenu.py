from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout, QWidget, QScrollArea
from logs.LogsConfig import *
from config.config import *


class ChapterChooserMenu(QFrame):
    """
    Cette classe est un menu QFrame permet d'afficher les chapitres.
    """
    BUTTONS_LENGTH = 620
    BUTTONS_HEIGHT = 50

    def __init__(self, chapter_amount):
        super().__init__()

        assert (chapter_amount > 0)

        self.buttons = []

        self.scroll_area_container = QWidget()
        self.scroll_area_container.setObjectName("scroll_area_container")

        self.layout = QVBoxLayout(self.scroll_area_container)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        for i in range(1, chapter_amount + 1):
            button = QPushButton(f"({i}) ...")
            button = QPushButton(f"({i}) ...")
            button.setEnabled(False)
            button.setFixedSize(self.BUTTONS_LENGTH, self.BUTTONS_HEIGHT)
            button.setFlat(False)
            button.setObjectName("chapter_chooser_button")
            self.buttons.append(button)
            self.layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addStretch(1)
        self.layout.setSpacing(20)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_area_container)
        self.scroll_area.setObjectName("scroll_area")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

        self.resize(800, 600)

    def set_chapter_title(self, chapter_index, title):
        self.buttons[chapter_index].setText(f"Chapitre {chapter_index + 1} : {title}")
        # self.buttons[chapter_index].setText(f"{title}")
        self.buttons[chapter_index].setEnabled(True)

    def get_enabled_buttons(self):
        result = []
        for i in range(len(self.buttons)):
            if self.buttons[i].isEnabled():
                result.append(self.buttons[i])
        return result
