from importlib import import_module

from PyQt6.QtCore import QTimer, QMutex
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QGridLayout, QFrame, QLabel, QTextEdit
from src.Block import Block
from src.RandomFirstMessage import RandomFirstMessage
from src.Snake import Snake
from src.frames.CongratulationsFrame import CongratulationsFrame
from src.threads.BlockAnimationThread import BlockAnimationThread
from logs.LogsConfig import *
from config.config import *

# importer les classes Level dynamiquement
for chapter_index, chapter in enumerate(CHAPTERS, start=1):
    for title, (start_level, end_level) in chapter.items():
        for level in range(start_level, end_level + 1):
            module_name = f"src.level.chapter{chapter_index}.Level{level}"
            class_name = f"Level{level}"
            try:
                imported_class = getattr(import_module(module_name), class_name)
                globals()[class_name] = imported_class
            except Exception:
                logging.warning(f"Impossible to import level \"{module_name}\"")


class Game(QFrame):
    """
    Cette classe permet de gérer tous les éléments de gameplay quand le joueur lance un niveau.
    """

    MAX_WIDTH = 670

    def __init__(self, code_editor, parent=None):
        super(Game, self).__init__(parent)

        if FILE_LOGGING:
            logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

        self.editor = code_editor

        self.block_init_count = None

        self.current_level = None

        # 0 par default
        self.current_level_number = 0

        # Représente le serpent qui se déplace sur le terrain
        self.snake = None

        # Représente les cases du terrain ou se déplace le snake
        self.blocks = None

        # Thread qui permet de faire changer l'état d'une case sur le terrain durant l'animation
        self.block_animation = BlockAnimationThread(self)

        # Représente les variables qui changent de valeur sur le terrain
        self.changing_variable_blocks = []
        self.variable_blocks = {}

        # True : le joueur peut exécuter le code, False : il ne peut pas
        self.canPlay = True

        self.layout = QVBoxLayout(self)
        self.board_layout = QGridLayout()
        self.board_layout.setContentsMargins(0, 0, 0, 0)
        self.board_layout.setSpacing(0)
        # self.layout.addStretch(1)

        self.constraint_text = QTextEdit(self)
        self.constraint_text.setReadOnly(True)
        self.constraint_text.setMaximumHeight(200)
        self.constraint_text.setMaximumWidth(self.MAX_WIDTH)
        self.constraint_text.setObjectName("contraints_text")

        self.constraint_title = QLabel(self)
        self.constraint_title.setText("Enoncé :")
        self.constraint_title.setObjectName("red_title")

        self.board_message_label = QLabel(NO_BOARD_MESSAGE)
        self.board_message_label.setObjectName("board_message")

        self.congratulation_frame = CongratulationsFrame(self)

        self.reset_button = QPushButton("Réinitialiser le terrain", self)
        self.reset_button.setObjectName("large_buttons")
        self.reset_button.setMaximumWidth(self.MAX_WIDTH)
        self.reset_button.clicked.connect(self.reset_current_level_button_action)

        self.layout.addWidget(self.constraint_title)
        self.layout.addWidget(self.constraint_text)
        self.layout.addLayout(self.board_layout)
        self.layout.addWidget(self.board_message_label)
        self.board_message_label.hide()
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(self.congratulation_frame)
        self.congratulation_frame.hide()

        logging.info("game initialized")

    def get_current_tutorial_text(self):
        if self.current_level is not None:
            return self.current_level.help_text
        return ""

    def stop_block_animation(self):
        if self.block_animation is not None:
            self.block_animation.stop()

    def delete_existing_blocks(self):
        for i in reversed(range(self.board_layout.count())):
            widget = self.board_layout.itemAt(i).widget()
            if widget is not None:
                self.board_layout.removeWidget(widget)
                # widget.deleteLater()

    def init_block_grid_layout(self):
        self.block_init_count = 0
        for y in range(ROW):
            for x in range(COL):
                self.block_init_count += 1
                block = Block(y, x, self)
                self.blocks[y][x] = block
                self.board_layout.addWidget(block.label, y, x)

    def init_level(self, level_number):

        self.delete_existing_blocks()

        # Réinitialiser les cases du terrain
        self.blocks = [[None for _ in range(COL)] for _ in range(ROW)]
        self.init_block_grid_layout()

        # Creation de l'objet level :
        try:
            level_class = globals()[f"Level{level_number}"]
            self.current_level = level_class(self)

            # Message aléatoire en console (pas de messages pour les niveaux 1 et 2)
            if self.current_level_number != level_number and level_number != 1 and level_number != 2:
                self.editor.console.set_text_with_simple_style(RandomFirstMessage.generate())
            else:
                self.editor.console.set_text_with_simple_style("Rien à signaler !")

            # self.editor.console.set_tutorial_text(self.current_level.help_text)
            self.constraint_text.setText(self.current_level.constraint_text)

            self.current_level.is_no_blocks_level = not self.exists_block_on_board()

            if self.current_level.is_no_blocks_level:
                self.board_message_label.show()
            else:
                self.board_message_label.hide()

            if self.changing_variable_blocks:
                self.block_animation.connect_blocks()
                self.block_animation.isRunning = True
                self.block_animation.start()

            logging.info(
                f"\'Level{level_number}\' created with no errors : length={COL} height={ROW} ({self.block_init_count} "
                f"blocks available)")

        except KeyError:
            logging.warning(f"attempted to initialize \'Level{level_number}\' but it does not exists")

        except Exception as e:
            logging.warning(f"attempted to initialize \'Level{level_number}\' with the following error \'{e}\'")

        self.current_level_number = level_number
        self.hide_congratulations_frame()
        self.editor.enable_execute_button()
        self.enable_reset_button()

    def add_variable_block(self, y, x, name, value):
        """
        Ajoute un Block de type variable aux coordonnées données. Ne fais rien si les coordonnées sont incorrectes.
        :param y:
        :param x:
        :param name: Nom de la variable.
        :param value: Valeur de la variable.
        """
        if 0 <= y < ROW and 0 <= x < COL:
            try:
                self.blocks[y][x].set_variable(name, value)
                self.variable_blocks.update({name: self.blocks[y][x]})
            except Exception as e:
                logging.error(f"Variable Block initialisation error occurred : \"{e}\"")

    def change_variable_block_value(self, name, new_value=None):
        """
        Change la valeur d'un Block de type variable sur le terrain en une valeur donnée.
        Ne fais rien si le Block variable n'existe pas.
        :param name:
        :param new_value:
        """
        name = name.strip()
        if name in self.variable_blocks:
            block = self.variable_blocks[name]
            block.change_value_variable(new_value)
            self.variable_blocks.update({name: block})

    def add_spawn_block(self, y, x):
        """
        Ajoute un Block de type point d'apparition avec un serpent dessus aux coordonnées données. Ne fais rien si les
        coordonnées sont incorrectes.
        :param y:
        :param x:
        """
        if 0 <= y < ROW and 0 <= x < COL:
            try:
                self.blocks[y][x].set_spawn()
                self.snake = Snake(self, y, x)
            except Exception as e:
                logging.error(f"Spawn Block initialisation error occurred : \"{e}\"")

    def add_block(self, y, x):
        """
        Ajoute un Block vide aux coordonnées données. Ne fais rien si les coordonnées sont incorrectes.
        :param y:
        :param x:
        """
        if 0 <= y < ROW and 0 <= x < COL:
            try:
                self.blocks[y][x].set_empty()
            except Exception as e:
                logging.error(f"Block initialisation error occurred : \"{e}\"")

    def add_destination_block(self, y, x):
        """
        Ajoute un Block de type point d'arrivée aux coordonnées données. Ne fais rien si les coordonnées
        sont incorrectes.
        :param y:
        :param x:
        """
        if 0 <= y < ROW and 0 <= x < COL:
            try:
                self.blocks[y][x].set_destination()
            except Exception as e:
                logging.error(f"Destination Block initialisation error occurred : \"{e}\"")

    def clear(self):
        """
        Retire toutes les valeurs des attributs de l'objet Game.
        """
        if self.current_level is not None:
            self.current_level = None
            self.current_level_number = None
            self.blocks = None
            self.snake = None
            self.canPlay = True

            self.changing_variable_blocks = []
            self.variable_blocks = {}
            logging.info(f"cleared \'Level{self.current_level_number}\'")

    def reset_current_level(self):
        """
        Réinitialise le niveau actuel de la partie en utilisant le dernier indice de niveau gardé en mémoire.
        """
        self.changing_variable_blocks = []
        self.variable_blocks = {}

        logging.info(f"attempt to reset \'Level{self.current_level_number}\'")
        self.init_level(self.current_level_number)

    def reset_current_level_button_action(self):
        """
        Action du bouton "réinitialiser le niveau"
        Permet de réinitialiser le niveau actuel de la partie en utilisant le dernier indice de niveau gardé en mémoire.
        Cette méthode permet de considérer les cas ou un thread d'animation est en cours de lancement et met fin à
        l'exécution de ce thread si c'est le cas.
        Lance une réinitialisation directe dans le cas ou aucun thread d'animation n'est en cours d'exécution.
        """
        if self.changing_variable_blocks:
            self.block_animation.stop()

        if self.snake is not None:
            self.snake.is_alive = False

        if not self.canPlay or self.editor.animation_thread.is_running:
            # Le joueur a lancé l'animation du serpent
            # Réinitialisation avec timer de sécurité (synchronisation des threads)
            if self.editor is not None and self.editor.animation_thread is not None:
                self.editor.disable_execute_button()
                self.disable_reset_button()

                self.editor.animation_thread.animation_speed = ENDING_ANIMATION_SPEED

                # Temps d'attente avant de réactiver les boutons pour éviter que l'utilisateur "spam" les boutons
                # ce qui pourraient engendrer des conflits de threads
                QTimer.singleShot(RESET_TIMER, self.reset_current_level)
                QTimer.singleShot(int(RESET_TIMER + (RESET_TIMER / 20)), self.editor.enable_execute_button)
                QTimer.singleShot(int(RESET_TIMER + (RESET_TIMER / 10)), self.enable_reset_button)

                logging.info(f"\'Level{self.current_level_number}\' was attempted to reset successfully")
            else:
                logging.error(
                    f"\'Level{self.current_level_number}\' was attempted to reset, but the editor is not initialized")
        else:
            # Réinitialisation directe dans le cas ou
            # le joueur réinitialise le niveau alors que l'animation du serpent n'a pas commencé / est terminée
            self.reset_current_level()
            self.editor.enable_execute_button()
            self.enable_reset_button()

            logging.info(f"\'Level{self.current_level_number}\' was attempted to reset successfully")

    def init_next_level(self):
        """
        Initialise le niveau suivant le niveau actuel, s'il n'existe pas ne fait rien.
        """
        self.current_level_number += 1
        self.init_level(self.current_level_number)

    def disable_reset_button(self):
        self.reset_button.setText("Réinitialisation en cours...")
        self.reset_button.setEnabled(False)
        logging.info("reset button disabled")

    def enable_reset_button(self):
        self.reset_button.setText("Réinitialiser le terrain")
        self.reset_button.setEnabled(True)
        logging.info("reset button enabled")

    def show_congratulations_frame(self):
        self.constraint_text.hide()
        self.constraint_title.hide()
        self.board_message_label.hide()
        self.reset_button.hide()
        self.congratulation_frame.show()
        # self.editor.hide()
        logging.info("congratulation frame shown")

    def hide_congratulations_frame(self):
        self.congratulation_frame.hide()
        if self.current_level is not None and self.current_level.is_no_blocks_level:
            self.board_message_label.show()
        self.constraint_text.show()
        self.constraint_title.show()
        self.reset_button.show()
        logging.info("congratulation frame hidden")

    def exists_block_on_board(self):
        """
        :return: True s'il existe au moins une case vide ou non sur le terrain, False sinon.
        Permet de déduire que le niveau actuel contient un terrain de jeu avec le serpent.
        """
        if self.blocks is not None or self.blocks == []:
            for block_row in self.blocks:
                for block in block_row:
                    if not block.is_removed:
                        return True
        return False
