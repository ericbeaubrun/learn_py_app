from PyQt6.QtCore import Qt
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame

# from Game import Game
from logs.LogsConfig import *


class CongratulationsFrame(QFrame):
    """
    Cette classe est un menu QFrame qui doit s'afficher quand le joueur a réussi un niveau.
    """

    CONGRATULATIONS_IMAGE_PATH = "res/congratulations.png"

    def __init__(self, game):
        assert (game is not None)
        super().__init__()
        if FILE_LOGGING:
            logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

        self.layout = QVBoxLayout()

        self.label = QLabel()
        # self.label = QLabel("Vous avez gagné !")
        self.label.setPixmap(QPixmap(self.CONGRATULATIONS_IMAGE_PATH))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("win_label")
        self.label.setWordWrap(True)

        self.next_level_button = QPushButton("Niveau suivant")
        self.next_level_button.setObjectName("large_buttons")
        self.next_level_button.setFixedHeight(30)

        self.restart_button = QPushButton("Recommencer")
        self.restart_button.setObjectName("large_buttons")
        self.restart_button.setFixedHeight(30)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.next_level_button)
        self.layout.addWidget(self.restart_button)

        self.setLayout(self.layout)

        self.connect_next_level_button(game)
        self.connect_restart_button(game)

        logging.info("congratulation frame initialized")

    def connect_next_level_button(self, game):
        self.next_level_button.clicked.connect(game.init_next_level)
        self.next_level_button.clicked.connect(game.editor.enable_execute_button)
        self.next_level_button.clicked.connect(game.enable_reset_button)
        self.next_level_button.clicked.connect(game.editor.clear)
        self.next_level_button.clicked.connect(game.hide_congratulations_frame)
        # congrat_frame.next_level_button.clicked.connect(self.editor.console.clear)

    def connect_restart_button(self, game):
        self.restart_button.clicked.connect(game.reset_current_level)
        self.restart_button.clicked.connect(game.hide_congratulations_frame)
