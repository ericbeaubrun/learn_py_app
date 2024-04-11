from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QHBoxLayout
from logs.LogsConfig import *
from src.level.LevelWonSaver import LevelWonSaver


class LevelChooserMenu(QFrame):
    """
    Cette classe est un menu QFrame permet d'afficher les niveaux.
    """

    BUTTONS_PER_LINE = 5
    LEVEL_DONE_ICON_PATH = "res/level_done.png"

    def __init__(self, first_level_index, last_level_index):
        super().__init__()
        if FILE_LOGGING:
            logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

        buttons_amount = last_level_index - first_level_index + 1
        assert (buttons_amount > 0)

        self.first_level_index = first_level_index
        self.last_level_index = last_level_index

        self.main_layout = QVBoxLayout(self)

        self.button_grid = []

        self.LEVEL_DONE_ICON = QIcon(self.LEVEL_DONE_ICON_PATH)

        i = first_level_index

        level_state_list = LevelWonSaver.read_list()

        for _ in range(int((buttons_amount + self.BUTTONS_PER_LINE - 1) / 5)):
            row_layout = QHBoxLayout()
            row_buttons = []
            for _ in range(self.BUTTONS_PER_LINE):
                if i <= last_level_index:
                    button = QPushButton(f"{i}", self)
                    if i in level_state_list:
                        button.setIcon(self.LEVEL_DONE_ICON)
                        button.setStyleSheet("background-color: #8a825d")
                        button.setIconSize(QSize(36, 36))
                else:
                    button = QPushButton("...", self)
                    button.setEnabled(False)
                button.setFlat(False)

                i += 1

                button.setObjectName("level_chooser_button")
                button.setFixedSize(150, 150)
                row_layout.addWidget(button)
                row_buttons.append(button)
            self.main_layout.addLayout(row_layout)
            self.button_grid.append(row_buttons)

        logging.info("level chooser menu initialized")

    def get_enabled_button_list(self):
        button_list = []
        for i in range(len(self.button_grid)):
            for j in range(len(self.button_grid[i])):
                if self.button_grid[i][j].isEnabled():
                    button_list.append(self.button_grid[i][j])
        return button_list

    def get_buttons_index(self):
        return range(self.first_level_index, self.last_level_index + 1)

    def get_total_amount_buttons(self):
        return len(self.get_buttons_index())

    def count_finished_levels(self):
        result = 0
        level_won_index_list = LevelWonSaver.read_list()
        if level_won_index_list != []:
            for i in self.get_buttons_index():
                if i in level_won_index_list:
                    result += 1
        return result
