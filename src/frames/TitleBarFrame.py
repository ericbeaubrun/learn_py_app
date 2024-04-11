from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QLabel

from config.config import *
from logs.LogsConfig import *


class TitleBarFrame(QFrame):
    """
    Cette classe contient les boutons au dessus de la fenetre pour revenir en arrière par exemple.
    """
    BACK_BUTTON_LEFT_SIDE = True

    TOP_BUTTON_SIZE = QSize(5, 5)
    TOP_BUTTONS_ICON_SIZE = QSize(40, 40)
    QUIT_BUTTON_ICON_PATH = 'res/quit_icon.png'
    MINIMIZE_BUTTON_ICON_PATH = 'res/minimize_icon.png'
    BACK_BUTTON_ICON_PATH = 'res/back_icon.png'

    def __init__(self, parent):
        super().__init__(parent)
        if FILE_LOGGING:
            logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

        self.setFixedHeight(41)
        self.setFixedWidth(SCREEN_LENGTH - 3)
        self.setObjectName("title_bar")

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(1)
        self.layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Bouton retourner en arriere
        self.back_button = QPushButton("", self)
        self.back_button.setObjectName("title_bar_button")
        self.back_button.setIcon(QIcon(self.BACK_BUTTON_ICON_PATH))
        self.back_button.setFixedSize(self.TOP_BUTTON_SIZE)
        self.back_button.setIconSize(self.TOP_BUTTONS_ICON_SIZE)
        self.back_button.setFixedSize(self.TOP_BUTTONS_ICON_SIZE)
        self.back_button.setFlat(False)

        if not self.BACK_BUTTON_LEFT_SIDE:
            self.layout.addWidget(self.back_button)

        self.title_label = QLabel("")
        self.title_label.setObjectName("title_label")
        self.layout.addWidget(self.title_label)

        self.setLayout(self.layout)

        logging.info("title bar frame initialized")

    def connect_title_bar_back_button(self, function):
        try:
            self.back_button.disconnect()
        except Exception as e:
            logging.error(f"title bar back button connection to \'{str(function)}\' failed")
        finally:
            self.back_button.clicked.connect(function)
