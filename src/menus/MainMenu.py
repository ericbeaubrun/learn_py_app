from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from logs.LogsConfig import *
from config.config import *


class MainMenu(QFrame):
    """
    Cette classe est un menu QFrame permet d'afficher les le menu principal du jeu.
    """
    BUTTONS_LENGTH = 210
    BUTTONS_HEIGHT = 50

    def __init__(self):
        super().__init__()
        if FILE_LOGGING:
            logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

        self.resize(SCREEN_LENGTH, SCREEN_HEIGHT)

        self.play_button = QPushButton(self)
        self.play_button.setFixedSize(self.BUTTONS_LENGTH, self.BUTTONS_HEIGHT)
        self.play_button.setText("JOUER")
        self.play_button.setObjectName("main_menu_play_button")

        self.help_button = QPushButton(self)
        self.help_button.setFixedSize(self.BUTTONS_LENGTH, self.BUTTONS_HEIGHT)
        self.help_button.setText("AIDE")
        self.help_button.setObjectName("main_menu_help_button")

        self.quit_button = QPushButton(self)
        self.quit_button.setFixedSize(self.BUTTONS_LENGTH, self.BUTTONS_HEIGHT)
        self.quit_button.setText("QUITTER")
        self.quit_button.setObjectName("main_menu_quit_button")

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(20)
        self.layout.addStretch(1)
        self.layout.addWidget(self.play_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.help_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.quit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

        logging.info("main menu initialized")
