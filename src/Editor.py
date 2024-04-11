from PyQt6.QtCore import QTimer, pyqtSignal, QMutex
from PyQt6.Qsci import QsciScintilla
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QFrame, QSplitter, QLabel
from PyQt6.QtCore import Qt

from src.EditorLexer import EditorLexer
from src.Game import Game
from src.threads.GameAnimationThread import GameAnimationThread
from src.threads.CodeExecutionThread import CodeExecutionThread
from src.code_process.CodeFormatter import CodeFormatter
from src.Console import Console
from logs.LogsConfig import *
from config.config import *


class Editor(QFrame):
    """
    Cette classe contient toutes les fonctionnalités de l'éditeur de code python, de l'exécution du code
    et des actions lancées par l'exécution du code de l'utilisateur.
    """

    EXECUTE_BUTTON_TEXT = "Exécuter le programme"

    # Signal lancé lorsque le code de l'utilisateur a réussi un niveau.
    # Ce signal sera connecté depuis la classe menus.MainWindow.py
    win_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        if FILE_LOGGING:
            logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

        # Objet Game lié à l'éditeur pour permettre à l'éditeur de code d'intéragir avec les différents éléments du jeu.
        self.game = None

        # Thread permettant d'éxécuter le code de l'utlisateur poru vérifier les erreurs de synthaxe et les boucles infini
        self.code_verif_exec_thread = CodeExecutionThread()
        self.code_verif_exec_thread.terminate_signal.connect(self.code_execution_finished)

        # Timer pour compter la durée d'exécution de 'code_verif_execution_thread'
        self.timeout_timer = QTimer(self)
        self.timeout_timer.timeout.connect(self.terminate_code_execution)

        # Console connectée à l'editeur, affiche les erreurs présentent dans le code lorsque l'utilisateur clique sur 'exécuter'
        self.console = Console()

        # Code présent dans l'éditeur au moment ou l'utilisateur clique sur 'exécuter'
        self.code = ""

        # Thread permettant l'animation du Snake sur le terrain de jeu
        self.animation_thread = GameAnimationThread(self)


        # Editeur de code avec affichage de la synthaxe en couleur.
        self.editor_sci = QsciScintilla(self)

        # Analyse lexicale de l'editeur (couleur synthaxe) :
        self.lexer = EditorLexer()
        self.editor_sci.setLexer(self.lexer)
        self.apply_editor_styles(self.editor_sci)
        self.setFixedWidth(500)

        # Bouton pour exécuter le code
        self.execute_button = QPushButton(self.EXECUTE_BUTTON_TEXT, self)
        self.execute_button.setObjectName("large_buttons")
        self.execute_button.clicked.connect(self.execute_code)

        # Ajoute l'éditeur et la console au splitter
        splitter = QSplitter(self)
        splitter.addWidget(self.editor_sci)
        splitter.addWidget(self.console)
        splitter.setOrientation(Qt.Orientation.Vertical)
        splitter.setSizes(SLIDER_DIMENSION)

        # title_label.setFrameStyle(QFrame.Shape.StyledPanel)  #Encadre
        editor_title = QLabel(self)
        editor_title.setText("EDITEUR PYTHON")
        editor_title.setObjectName("green_title")

        layout = QVBoxLayout(self)
        layout.addWidget(editor_title)
        layout.addWidget(splitter)
        layout.addWidget(self.execute_button)
        logging.info("editor initialized")

    def link_to_game(self, game):
        assert (isinstance(game, Game))
        self.game = game

    def apply_editor_styles(self, editor_sci):
        """
        Applique le style de l'éditeur QScintilla.
        @param editor_sci: Editeur QScintilla.
        """
        editor_sci.setObjectName("editor")
        editor_sci.setCaretLineVisible(True)
        editor_sci.setTabWidth(4)
        editor_sci.setIndentationWidth(4)
        editor_sci.setIndentationsUseTabs(True)
        editor_sci.setMarginWidth(0, "0000")
        editor_sci.setMarginLineNumbers(0, True)
        editor_sci.setCaretForegroundColor(QColor("#f8f8f2"))
        editor_sci.setMarginsBackgroundColor(QColor("#2b2b2b"))
        editor_sci.setMarginsForegroundColor(QColor("#f8f8f2"))
        editor_sci.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        editor_sci.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        editor_sci.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        editor_sci.setCaretLineBackgroundColor(QColor("#3e3d32"))

    def clear(self):
        """
        Retire le contenu textuel de l'éditeur de code.
        """
        self.editor_sci.clear()

    def enable_execute_button(self):
        if self.game is not None:
            self.execute_button.setDisabled(False)
            self.execute_button.setText(self.EXECUTE_BUTTON_TEXT)
            logging.info("execute button enabled")
            # self.console.set_text_with_simple_style("Réinitialisation du niveau "
            # + str(self.game.current_level_number) + " effectuée")

    def disable_execute_button(self):
        self.execute_button.setText("...")
        self.execute_button.setDisabled(True)
        logging.info("execute button disabled")

    def code_execution_finished(self, output):
        """
        Cette méthode se lance lorsque la première exécution du code python de l'utilisateur est terminée. Elle
        permet de lancer l'exécution du thread de l'animation du jeu.
        Et elle permet aussi d'afficher en console les erreurs de synthaxe s'il y en a.
        @param output: Chaine de caractère qui permet de savoir ce qu'il s'est passé durant la
        première exécution du code python de l'utilisateur.
        """
        if isinstance(output, Exception):
            self.console.set_text_with_error_style(f"Erreur: {str(output)}")
            logging.info(f"user code has been executed with following error :\n{str(output)}")
        else:
            self.console.clear()
            # self.console.append_text_with_simple_style("Pas d'erreur à signaler !")
            self.console.append_text_with_simple_style(self.code_verif_exec_thread.captured_output)

            self.code = CodeFormatter.format_code(self.editor_sci.text())
            self.animation_thread.connect_signals()
            self.animation_thread.start()
            self.disable_execute_button()
            logging.info("user code has been executed with no error")

    def animation_finished(self):
        # Si le niveau demande de faire des déplacements (avec un Snake)
        snake = self.game.snake
        current_level = self.game.current_level
        output = self.game.editor.code_verif_exec_thread.captured_output
        code = self.code

        # Vérification que le joueur respecte bien les contraintes de niveau.
        output_validation = current_level.validate_output(output)
        code_validation = current_level.validate_code(code)

        if snake is not None:
            if snake.movement_count == 0:
                # Dans le cas ou le Snake ne s'est pas déplacé.

                if self.game.exists_block_on_board() and code_validation != VALID_CODE_MESSAGE:
                    self.console.append_text_with_invalid_style(code_validation)

                # elif snake.has_reached_destination and snake.is_alive:
                #     self.console.append_text_with_simple_style(VALID_CODE_MESSAGE + "\n" + VALID_OUTPUT_MESSAGE)
                #     self.win_signal.emit()

                else:
                    self.enable_execute_button()
            else:
                if (snake.has_reached_destination and snake.is_alive
                        and output_validation == VALID_OUTPUT_MESSAGE
                        and code_validation == VALID_CODE_MESSAGE):
                    self.console.append_text_with_simple_style(VALID_CODE_MESSAGE + "\n" + VALID_OUTPUT_MESSAGE)
                    self.win_signal.emit()

                elif output_validation != VALID_OUTPUT_MESSAGE:
                    self.console.append_text_with_invalid_style(INVALID_OUTPUT_MESSAGE)

                elif code_validation != VALID_CODE_MESSAGE:
                    self.console.append_text_with_invalid_style(code_validation)
                self.disable_execute_button()

        else:
            # Si le niveau ne demande pas de faire des déplacements (pas de Snake)
            if code_validation == VALID_CODE_MESSAGE and output_validation == VALID_OUTPUT_MESSAGE:
                self.disable_execute_button()
                self.console.append_text_with_simple_style(VALID_CODE_MESSAGE + "\n" + VALID_OUTPUT_MESSAGE)
                self.win_signal.emit()
            else:
                if code_validation != VALID_CODE_MESSAGE:
                    self.console.append_text_with_invalid_style(code_validation)
                elif output_validation != VALID_OUTPUT_MESSAGE:
                    self.console.append_text_with_invalid_style(output_validation)

                self.enable_execute_button()

    def terminate_code_execution(self):
        """
        Met fin à la première exécution du code en cas de problème / boucle infinie.
        """
        if self.code_verif_exec_thread.isRunning():
            self.code_verif_exec_thread.terminate()
            self.console.set_text_with_error_style("Votre programme semble contenir une boucle infini !")
            logging.info(f"code execution has been terminated due to timeout ({EXEC_TIMEOUT}ms)")

    def execute_code(self):
        """
        Permet de lancer une première exécution du code présent dans l'éditeur de code QSCintilla pour
        vérifier qu'il ne contient pas d'erreurs.
        Lance un Thread pour le timer qui permet de vérifier que le code ne contient pas de boucle infinie.
        """
        if self.game is not None:
            if self.game.canPlay and self.editor_sci.text() != "":
                self.console.clear()
                self.console.appendPlainText("Vérification du code...")

                self.code = CodeFormatter.append_variable_declarations(self.game.variable_blocks,
                                                                       self.editor_sci.text())
                self.code_verif_exec_thread.code = self.code

                # self.code_verif_exec_thread.code = self.editor_sci.text()
                self.timeout_timer.start(EXEC_TIMEOUT)
                self.code_verif_exec_thread.start()

            elif self.game.canPlay:
                logging.warning("attempted to execute code without permission to play")

            elif self.editor_sci.text():
                logging.info("attempted to execute an empty code")
        else:
            logging.error("attempted to execute code with no game initialized")

    def print_solution(self):
        """
        Ecrit dans l'éditeur de code la solution venant du niveau actuel.
        """
        level = self.game.current_level
        if level is not None and level.possible_solution is not None:
            self.editor_sci.setText(level.possible_solution)
