from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from logs.LogsConfig import *


class Block:
    """
    Cette classe représente une case sur le terrrain de jeu, elle peut encapsuler les informations de n'importe quelle type de case.
    """
    BLOCK_HEIGHT = 50
    BLOCK_WIDTH = 50

    BACKGROUND_COLOR = "#3a3a3a"

    SPAWN_COLOR_1 = '#6a6a6a'
    SPAWN_COLOR_2 = '#5b5b5b'

    EMPTY_COLOR_1 = '#6a6a6a'
    EMPTY_COLOR_2 = '#5b5b5b'

    VARIABLE_COLOR_1 = "#8a7e5e"
    VARIABLE_COLOR_2 = "#736b56"

    DESTINATION_COLOR = '#a6e22e'

    def __init__(self, y, x, parent=None):
        self.y = y
        self.x = x

        self.label_text = ""
        self.label = QLabel(self.label_text, parent)
        self.label.setFixedSize(self.BLOCK_HEIGHT, self.BLOCK_WIDTH)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setAutoFillBackground(True)

        self.has_changing_value = False
        self.current_value_index = 0
        self.changing_values = []
        self.is_secret_value = False

        self.is_spawn = False
        self.is_removed = True
        self.passage_to_win = 0

        self.variable_name = ""
        self.variable_value = ""

        self.palette = self.label.palette()
        self.palette.setColor(QPalette.ColorRole.Window, QColor(self.BACKGROUND_COLOR))
        self.label.setPalette(self.palette)
        # self.is_enough_to_win = False
        # self.teleport_to = None

    def set_spawn(self):
        """
        Permet de définir ce Block en tant que point d'apparition pour le serpent.
        """
        self.is_removed = False
        self.is_spawn = True

        if (self.x + self.y) % 2 != 0:
            self.palette.setColor(QPalette.ColorRole.Window, QColor(self.SPAWN_COLOR_1))
        else:
            self.palette.setColor(QPalette.ColorRole.Window, QColor(self.SPAWN_COLOR_2))

        self.label.setPalette(self.palette)
        self.label.setText("")

    def set_empty(self):
        """
        Permet de définir ce Block en tant que Block basique sans attributs particuliers.
        """
        self.variable_name = ""
        self.variable_value = ""
        self.is_removed = False
        self.is_spawn = False

        if (self.x + self.y) % 2 != 0:
            self.palette.setColor(QPalette.ColorRole.Window, QColor(self.EMPTY_COLOR_1))
        else:
            self.palette.setColor(QPalette.ColorRole.Window, QColor(self.EMPTY_COLOR_2))

        self.label.setPalette(self.palette)
        self.label.setText("")

    def set_variable(self, name, value):
        """
        Permet de définir ce block en tant que Block de variable, avec un style de variable et un texte à l'intérieur.
        :param name: Nom de la variable.
        :param value: Valeur de la variable.
        """
        self.variable_name = name
        self.variable_value = value

        self.is_removed = False
        self.is_spawn = False

        self.label_text = f"{name}"

        if value is not None:
            self.label_text += f"\n=\n{value}"
            self.label.setToolTipDuration(0)
            self.label.setToolTip(str(value))
            if (self.x + self.y) % 2 != 0:
                self.palette.setColor(QPalette.ColorRole.Window, QColor(self.VARIABLE_COLOR_1))
            else:
                self.palette.setColor(QPalette.ColorRole.Window, QColor(self.VARIABLE_COLOR_2))
            self.label.setStyleSheet('color: white;')
        else:
            self.label.setToolTip("")
            self.add_border()

        self.label.setPalette(self.palette)

        self.label.setText(self.label_text)

    def add_border(self):
        """
        Ajoute une bordure pointillée à un Block.
        """
        self.palette.setColor(QPalette.ColorRole.Window, QColor(self.BACKGROUND_COLOR))
        self.label.setStyleSheet(f"color: white; "
                                 f"border: 2px solid white; "
                                 f"border-style: dotted; "
                                 f"margin: 2px;")
        self.label.setPalette(self.palette)

    def remove_border(self):
        """
        Retire la bordure pointillée d'un Block.
        """
        self.label.setStyleSheet("")
        if (self.x + self.y) % 2 != 0:
            self.palette.setColor(QPalette.ColorRole.Window, QColor(self.VARIABLE_COLOR_1))
        else:
            self.palette.setColor(QPalette.ColorRole.Window, QColor(self.VARIABLE_COLOR_2))
        self.label.setPalette(self.palette)

    def change_value_variable(self, value):
        """
        :param value: La nouvelle valeur de la variable.
        """
        self.label_text = f"{self.variable_name}"

        if value is not None:
            self.label_text += f"\n=\n{value}"
            self.label.setToolTipDuration(0)
            self.label.setToolTip(str(value))
            self.remove_border()
        else:
            self.add_border()
            self.label.setToolTip("")

        self.label.setText(self.label_text)


    def set_destination(self):
        """
        Cette méthode permet de determiner ce Block en tant que destination. Le Snake gagnera s'il atteint ce Block.
        """
        self.variable_name = ""
        self.variable_value = ""

        self.is_removed = False
        self.is_spawn = False
        self.passage_to_win = 1

        self.palette.setColor(QPalette.ColorRole.Window, QColor(self.DESTINATION_COLOR))
        self.label.setPalette(self.palette)

        self.label.setText("")

    def next_changing_value(self):
        """
        Cette fonction n'est pas terminée.
        """
        if self.has_changing_value:
            if self.current_value_index < len(self.changing_values) - 1:
                self.current_value_index += 1
            else:
                self.current_value_index = 0
            self.label_text = (f"{self.variable_name}"
                               f"\n=\n"
                               f"{self.changing_values[self.current_value_index]}")

            try:
                self.label.setStyleSheet('color: white;')

                if self.current_value_index % 3 == 0:
                    self.palette.setColor(QPalette.ColorRole.Window, QColor('#475231'))
                elif self.current_value_index % 3 == 1:
                    self.palette.setColor(QPalette.ColorRole.Window, QColor('#31523a'))
                else:
                    self.palette.setColor(QPalette.ColorRole.Window, QColor('#524831'))

                self.label.setPalette(self.palette)
                self.label.setText(self.label_text)
            except:
                print("ERREUR STYLESHEET")


        # def set_changing_value_variable(self, name, values):
        #     assert (len(values) > 0)
        #     self.has_changing_value = True
        #
        #     self.variable_name = name
        #     self.changing_values = values
        #
        #     self.is_removed = False
        #     self.is_spawn = False
        #
        #     self.label_text = (f"{self.variable_name}"
        #                        f"\n=\n"
        #                        f"{self.changing_values[0]}")