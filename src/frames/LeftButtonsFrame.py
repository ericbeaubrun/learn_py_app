from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QSizePolicy
from logs.LogsConfig import *
from config.config import *


class LeftButtonsFrame(QFrame):
    """
    Cette classe est un QFrame qui contient les boutons d'actions dans le jeu.
    """
    def __init__(self, main_window):
        super().__init__()
        buttons_layout = QVBoxLayout(self)

        for text in LEFT_BUTTONS_TEXT:
            button = QPushButton(text, self)
            button.setObjectName("left_buttons")
            button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            button.setFixedWidth(100)
            button.setFixedHeight(65)
            self.connect_left_button(main_window, button)
            buttons_layout.addWidget(button)
        buttons_layout.setContentsMargins(5, 35, 15, 0)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)

        logging.info("left buttons frame initialized")

    def connect_left_button(self, main_window, button):
        """
        Connecte un bouton présent sur la partie gauche de l'écran durant la partie à l'action qui doit lui être est
        associée (dependement du texte du bouton).

        @param button: Le bouton dont on veut ajouter une action.
        """
        editor = main_window.code_editor
        match button.text():
            case 'Ralentir':
                button.clicked.connect(editor.animation_thread.increase_animation_speed)
                # button.clicked.connect(main_window.code_editor.print_animation_speed)
                button.clicked.connect(
                    lambda: editor.console.print_animation_speed(editor.animation_thread.animation_speed))

            case 'Accélérer':
                button.clicked.connect(editor.animation_thread.decrease_animation_speed)
                # button.clicked.connect(editor.print_animation_speed)
                button.clicked.connect(
                    lambda: editor.console.print_animation_speed(editor.animation_thread.animation_speed))
            case 'Menu':
                button.clicked.connect(main_window.show_menu)

            case 'Aide':
                button.clicked.connect(lambda: editor.console.set_tutorial_text(
                    main_window.game.get_current_tutorial_text()))

            case 'Solution':
                button.clicked.connect(editor.print_solution)

            case 'Clear':
                button.clicked.connect(editor.clear)

            case '...':
                button.setEnabled(False)
