from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from src.Editor import Editor
from src.Game import Game
from config.config import *
from src.level.LevelWonSaver import LevelWonSaver
from src.frames.LeftButtonsFrame import LeftButtonsFrame
from src.menus.LevelChooserMenu import LevelChooserMenu
from src.menus.ChapterChooserMenu import ChapterChooserMenu
from src.menus.MainMenu import MainMenu
from logs.LogsConfig import *
from src.frames.TitleBarFrame import TitleBarFrame


class MainWindow(QMainWindow):
    """
    Cette classe est un menu QFrame qui encapsule tous les composant graphiques qui sont affichés sur la fenêtre du logiciel.
    """

    WINDOW_TITLE = 'Projet Python L3 Groupe 1'

    ICON_PATH = "res/logo.ico"

    LEVEL_DONE_ICON_PATH = "res/level_done.png"

    def __init__(self):
        super().__init__()
        if FILE_LOGGING:
            logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

        self.setGeometry(30, 100, SCREEN_LENGTH, SCREEN_HEIGHT)
        self.setFixedSize(SCREEN_LENGTH, SCREEN_HEIGHT)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, FRAMELESS_HINT)
        self.setWindowIcon(QIcon(self.ICON_PATH))
        self.setWindowTitle(self.WINDOW_TITLE)
        self.central_widget = QWidget()
        self.central_widget.setObjectName("background")
        self.setCentralWidget(self.central_widget)

        # Creation de la barre de titre
        self.title_bar = TitleBarFrame(self)
        # self.title_bar = TitleBar()

        # Creation des layouts
        self.horizontal_layout = QHBoxLayout(self.central_widget)
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.title_bar)
        self.vertical_layout.addLayout(self.horizontal_layout)

        # Creation de l'interface de jeu (éditeur de code et terrain de jeu)
        self.code_editor = Editor()
        self.game = Game(self.code_editor)
        self.code_editor.link_to_game(self.game)
        self.left_buttons_frame = LeftButtonsFrame(self)

        # Creation du menu principal
        self.main_menu = MainMenu()
        self.main_menu.play_button.clicked.connect(self.show_chapter_chooser)
        self.main_menu.quit_button.clicked.connect(self.close)

        # Creation du menu de choix de chapitres et de niveaux
        self.level_chooser_list = []
        self.chapter_chooser_menu = None
        self.current_level_chooser = None
        self.current_chapter_index = 0
        self.init_chapters_and_levels()

        self.title_bar.connect_title_bar_back_button(lambda: None)

        self.game.congratulation_frame.next_level_button.clicked.connect(
            lambda: self.title_bar.title_label.setText(f" Niveau {self.game.current_level_number} "))

        self.code_editor.win_signal.connect(lambda: LevelWonSaver.append(self.game.current_level_number))
        self.code_editor.win_signal.connect(lambda: self.set_level_done(self.game.current_level_number))
        self.code_editor.win_signal.connect(self.code_editor.game.show_congratulations_frame)

        # Ajout des widgets à la fenêtre principale
        self.horizontal_layout.addWidget(self.left_buttons_frame)
        self.horizontal_layout.addWidget(self.main_menu)
        self.horizontal_layout.addWidget(self.chapter_chooser_menu)
        for level_chooser in self.level_chooser_list:
            self.horizontal_layout.addWidget(level_chooser)
            level_chooser.hide()
        self.horizontal_layout.addWidget(self.code_editor)
        self.horizontal_layout.addWidget(self.game)

        self.assert_all_frames_exists()

        self.main_menu.show()

        self.title_bar.title_label.hide()
        self.current_level_chooser.hide()
        self.chapter_chooser_menu.hide()
        self.left_buttons_frame.hide()
        self.code_editor.hide()
        self.game.hide()

        logging.info("main window initialized")

    def find_enabled_button_level(self, level_index):
        """
        Retourne le bouton associé à l'indice pris en parametre en parcourant tous les chapitres
        Si le bouton existe et est activé alors il est renvoyé sinon retourne None.
        :param level_index: l'indice du bouton de niveau à retrouver
        """
        i = 0
        while i < len(self.level_chooser_list):
            button_list = self.level_chooser_list[i].get_enabled_button_list()

            for j in range(len(button_list)):
                level_index -= 1
                if level_index == 0:
                    return button_list[j]
            i += 1
        return None

    def set_level_done(self, level_index):
        """
        Parcours tous les niveaux pour trouver celui qui a l'indice donné et lui ajoute l'icon
        de niveau terminé. Ne fais rien si l'indice de niveau est incorrect.
        :param level_index: L'indice du niveau terminé.
        """
        button = self.find_enabled_button_level(level_index)
        if button is not None:
            assert (isinstance(button, QPushButton))
            button.setIcon(QIcon(self.LEVEL_DONE_ICON_PATH))
            button.setIconSize(QSize(36, 36))
            button.setStyleSheet("background-color: #8a825d")
        self.refresh_chapter_buttons_done()

    def add_chapter(self, title, first_level_index, last_level_index):
        """
        Ajoute un chapitre et le li aux niveaux selon les indices de niveaux donnés.
        :param title: Titre du chapitre.
        :param first_level_index: Indice du premier niveau du chapitre.
        :param last_level_index: Indice du dernier niveau du chapitre.
        """
        if last_level_index > first_level_index:
            self.chapter_chooser_menu.set_chapter_title(len(self.level_chooser_list), title)
            self.level_chooser_list.append(LevelChooserMenu(first_level_index, last_level_index))

    def init_chapters_and_levels(self):
        """
        Crée tous les chapitres et tous les niveaux associés en se basant sur le tableau CHAPTERS dans le fichier config.
        """
        self.chapter_chooser_menu = ChapterChooserMenu(MAX_AMOUNT_CHAPTERS)

        for chapter_data in CHAPTERS:
            chapter_name, level_numbers = list(chapter_data.items())[0]
            self.add_chapter(chapter_name, level_numbers[0], level_numbers[1])
            logging.info(f"chapter \"{chapter_name}\" button created for levels {level_numbers[0]}-{level_numbers[1]}")

        self.connect_chapter_chooser_buttons()
        self.current_level_chooser = self.level_chooser_list[0]
        self.connect_level_chooser_buttons()

        self.refresh_chapter_buttons_done()

    def connect_chapter_chooser_buttons(self):
        """
        Connecte tous les boutons du menu de choix de chapitre à la méthode d'initialisation.
        """
        for i in range(0, len(self.level_chooser_list), 1):
            self.chapter_chooser_menu.buttons[i].clicked.connect(lambda _, index=i: self.show_level_chooser(index))
            logging.info(f"chapter choose button {i} connected to level chooser {i}")

    def connect_level_chooser_buttons(self):
        """
        Connecte tous les boutons du menu de choix de niveaux à la méthode d'initialisation.
        """
        i = 0
        for level_chooser in self.level_chooser_list:
            for button_list in level_chooser.button_grid:
                for button in button_list:
                    assert (isinstance(button, QPushButton))
                    if button.isEnabled():
                        i += 1
                        button.clicked.connect(lambda _, level_index=i: self.game.init_level(level_index))
                        button.clicked.connect(self.show_game)

                        logging.info(f"button \'{button.text()}\' connected to \'Level{i}\'")

    def refresh_chapter_buttons_done(self):
        """
        Met à jour le style des boutons de chapitre lorsque tous les niveaux de chapitre ont été terminés.
        """
        buttons = self.chapter_chooser_menu.get_enabled_buttons()
        for i in range(len(buttons)):
            level_chooser = self.level_chooser_list[i]
            finished = level_chooser.count_finished_levels()
            total = level_chooser.get_total_amount_buttons()

            if finished == total:
                button = buttons[i]
                button.setIcon(QIcon(self.LEVEL_DONE_ICON_PATH))
                button.setIconSize(QSize(26, 26))
                button.setStyleSheet("background-color: #8a825d; text-decoration: line-through;")

    def show_menu(self):
        """
        Affiche le menu principal uniquement.
        """
        self.assert_all_frames_exists()

        self.title_bar.connect_title_bar_back_button(lambda: None)

        self.title_bar.title_label.hide()
        self.chapter_chooser_menu.hide()
        self.current_level_chooser.hide()
        self.left_buttons_frame.hide()
        self.code_editor.hide()
        self.game.hide()

        self.main_menu.show()

        self.code_editor.clear()
        self.game.clear()

        logging.info("menu frame shown")

    def show_level_chooser(self, index):
        """
        Affiche le menu de choix de niveaux uniquement.
        :param index: L'indice de la page de choix de niveau à afficher.
        """
        self.assert_all_frames_exists()

        self.title_bar.connect_title_bar_back_button(self.show_chapter_chooser)

        self.current_level_chooser.hide()
        self.current_level_chooser = self.level_chooser_list[index]
        self.current_chapter_index = index + 1

        self.title_bar.title_label.show()
        self.title_bar.title_label.setText(f" Chapitre {self.current_chapter_index} ")

        self.chapter_chooser_menu.hide()
        self.left_buttons_frame.hide()
        self.code_editor.hide()
        self.main_menu.hide()
        self.game.hide()

        self.code_editor.clear()
        self.game.clear()

        self.current_level_chooser.show()

        logging.info("level chooser frame shown")

    def show_current_level_chooser(self):
        """
        Affiche le menu de choix de niveaux du niveau lancé, si aucun niveau n'est lancé, affiche
        le dernier menu de choix de niveau affiché.
        """
        self.show_level_chooser(self.current_chapter_index - 1)

    def show_game(self):
        """
        Affiche l'interface du jeu.
        """
        self.assert_all_frames_exists()

        self.title_bar.connect_title_bar_back_button(self.show_current_level_chooser)

        self.current_level_chooser.hide()
        self.main_menu.hide()
        self.chapter_chooser_menu.hide()

        self.title_bar.title_label.show()
        self.title_bar.title_label.setText(f" Niveau {self.game.current_level_number} ")

        self.game.show()
        self.code_editor.show()
        self.left_buttons_frame.show()

        logging.info("game frame shown")

    def show_chapter_chooser(self):
        """
        Affiche le menu de choxi de chapitres.
        """
        self.assert_all_frames_exists()

        self.title_bar.connect_title_bar_back_button(self.show_menu)

        self.current_level_chooser.hide()
        self.left_buttons_frame.hide()
        self.code_editor.hide()
        self.main_menu.hide()
        self.game.hide()

        self.title_bar.title_label.hide()

        self.code_editor.clear()
        self.game.clear()

        self.chapter_chooser_menu.show()

        logging.info("chapter chooser frame shown")

    def assert_all_frames_exists(self):
        """
        Vérifie que toutes les pages du logiciel existent et sont du bon type.
        """
        assert (self.game is not None and isinstance(self.game, Game))
        assert (self.main_menu is not None and isinstance(self.main_menu, MainMenu))
        assert (self.title_bar is not None and isinstance(self.title_bar, TitleBarFrame))
        assert (self.code_editor is not None and isinstance(self.code_editor, Editor))
        assert (self.left_buttons_frame is not None and isinstance(self.left_buttons_frame, LeftButtonsFrame))
        assert (self.chapter_chooser_menu is not None and isinstance(self.chapter_chooser_menu, ChapterChooserMenu))
        assert (self.current_level_chooser is not None and isinstance(self.current_level_chooser, LevelChooserMenu))
