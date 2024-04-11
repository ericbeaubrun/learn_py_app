from PyQt6.QtCore import QThread, pyqtSignal

from config.config import VALID_CODE_MESSAGE
from src import Editor
from logs.LogsConfig import *


class GameAnimationThread(QThread):
    """
    Cette classe permet de gérer toutes les animations du terrain de jeu (déplacements du serpent,
    assignation de variables)
    """

    # Constantes pour gérer la vitesse d'animation
    INITIAL_ANIMATION_SPEED = 500
    MAX_ANIMATION_SPEED = 900
    MIN_ANIMATION_SPEED = 200
    STEP_ANIMATION_SPEED = 200

    # Définition pour déplacer le serpent
    forward_signal = pyqtSignal()
    behind_signal = pyqtSignal()
    right_signal = pyqtSignal()
    left_signal = pyqtSignal()

    assignment_signal = pyqtSignal(str, object)

    finished_signal = pyqtSignal()

    def __init__(self, editor):
        assert (editor is not None)
        assert (isinstance(editor, Editor.Editor))

        super().__init__()
        if FILE_LOGGING:
            logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

        self.editor = editor
        # self.finished_signal.connect(self.editor.animation_finished)
        self.signals_are_connected = False
        self.is_running = False

        self.finished_signal.connect(self.editor.animation_finished)

        self.animation_speed = self.INITIAL_ANIMATION_SPEED
        self.last_animation_speed = self.INITIAL_ANIMATION_SPEED

    def connect_signals(self):
        """
        Connecte tous les signaux permettant d'afficher les déplacements du serpent sur l'interface graphique.
        """
        game = self.editor.game
        if game is not None and game.snake is not None and not self.signals_are_connected:
            # self.signals_are_connected = True
            self.forward_signal.connect(game.snake.go_ahead)
            self.behind_signal.connect(game.snake.go_behind)
            self.right_signal.connect(game.snake.turn_right)
            self.left_signal.connect(game.snake.turn_left)
            self.assignment_signal.connect(self.editor.game.change_variable_block_value)

            logging.info("snake animation moves signals has been connected")
        else:
            logging.info("unable to connect snake moves signals animation")

    def forward_animation(self):
        """
        Envoie un signal pour que le serpent avance d'une case sur l'interface graphique.
        """
        snake = self.editor.game.snake
        if snake is not None and snake.is_alive:
            self.forward_signal.emit()
            QThread.msleep(self.animation_speed)

    def back_animation(self):
        """
        Envoie un signal pour que le serpent se retourne sur l'interface graphique.
        """
        snake = self.editor.game.snake
        if snake is not None and snake.is_alive:
            self.behind_signal.emit()
            QThread.msleep(self.animation_speed)

    def right_animation(self):
        """
        Envoie un signal pour que le serpent tourne à droite sur l'interface graphique.
        """
        snake = self.editor.game.snake
        if snake is not None and snake.is_alive:
            self.right_signal.emit()
            QThread.msleep(self.animation_speed)

    def left_animation(self):
        """
        Envoie un signal pour que le serpent tourne à gauche sur l'interface graphique.
        """
        snake = self.editor.game.snake
        if snake is not None and snake.is_alive:
            self.left_signal.emit()
            QThread.msleep(self.animation_speed)

    def go_behind_animation(self):
        """
        Envoie plusieurs signaux pour que le serpent recule d'une case sur l'interface graphique.
        """
        self.back_animation()
        self.forward_animation()

    def increase_animation_speed(self):
        """
        Augmente la vitesse d'animation sans dépasser la valeur maximale définie en tant qu'attribut de classe.
        """
        if self.animation_speed < self.MAX_ANIMATION_SPEED:
            self.animation_speed += self.STEP_ANIMATION_SPEED
            logging.info(f"animation speed set to '{self.animation_speed}'")
        else:
            logging.warning(f"attempt to increase snake animation speed above {self.MAX_ANIMATION_SPEED}")

    def decrease_animation_speed(self):
        """
        Réduit la vitesse d'animation sans dépasser la valeur minimale définie en tant qu'attribut de classe.
        """
        if self.animation_speed > self.MIN_ANIMATION_SPEED:
            self.animation_speed -= self.STEP_ANIMATION_SPEED
            logging.info(f"animation speed set to '{self.animation_speed}'")
        else:
            logging.warning(f"attempt to decrease snake animation speed below {self.MIN_ANIMATION_SPEED}")

    def assignment(self, variable_name, value):
        """
        Permet de changer la valeur d'une variable sur le terrain de jeu.
        @param variable_name: Nom de la variable qui doit être assignée
        @param value: Valeur qui sera prise par la variable
        """
        if variable_name in self.editor.game.variable_blocks:
            self.assignment_signal.emit(variable_name, value)
            QThread.msleep(self.animation_speed)

    def run(self):
        self.is_running = True
        logging.info("snake animation started")
        valid_code = self.editor.game.current_level.validate_code(self.editor.code)
        if valid_code != VALID_CODE_MESSAGE:
            self.is_running = False

        if self.is_running:
            try:
                assert (self.editor is not None and isinstance(self.editor, Editor.Editor))

                # Exécution du code
                exec(self.editor.code)

                # Changement de la vitesse du jeu à la dernière vitesse mise.
                # Permet donc de récupérer une vitesse normale dans le cas ou la vitesse a été changée
                # pour terminer l'exécution du thread plus rapidement.
                self.animation_speed = self.last_animation_speed

                logging.info(f"the following instructions has been successfully executed :\n{self.editor.code}")
                logging.info(f"animation speed set to '{self.animation_speed}'")

            except Exception as e:
                self.is_running = False
                logging.error(f"the following error occured during snake animation :\n{e}")

            self.is_running = False
            logging.info("snake animation finished")
            # Exécution terminée, emet un signal pour effectuer le reste des actions dans la classe Editor
        self.finished_signal.emit()
