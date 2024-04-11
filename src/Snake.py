from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, pyqtSignal

from config.config import *
from logs.LogsConfig import *


class Snake:
    """
    Cette classe permet de représenter le personnage que le joueur controle (le serpent), elle encapsule les coordonnées et la directions du personnage.
    """

    # chemin de l'image du Snake
    SNAKE_PATH = "res/snake.png"

    # chemin de l'image du Snake quand il meurt
    SNAKE_PATH_DEAD = "res/snake_dead.png"

    SNAKE_LENGTH = 50 + 5
    SNAKE_HEIGHT = 50 + 5

    def __init__(self, game, y, x):
        if FILE_LOGGING:
            logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)
        self.game = game

        self.movement_count = 0
        self.is_alive = True
        self.has_reached_destination = False

        self.y = y
        self.x = x
        self.current_direction = 'right'

        self.snake_image = QPixmap(self.SNAKE_PATH).scaled(self.SNAKE_LENGTH, self.SNAKE_HEIGHT,
                                                           Qt.AspectRatioMode.KeepAspectRatio)

        self.snake_image_dead = QPixmap(self.SNAKE_PATH_DEAD).scaled(
            self.SNAKE_LENGTH, self.SNAKE_HEIGHT,
            Qt.AspectRatioMode.KeepAspectRatio)

        self.snake_label = QLabel(self.game)

        self.snake_label.setPixmap(QPixmap(self.SNAKE_PATH).scaled(self.SNAKE_LENGTH, self.SNAKE_HEIGHT,
                                                                   Qt.AspectRatioMode.KeepAspectRatio))
        self.game.board_layout.addWidget(self.snake_label, self.y, self.x)

        logging.info(f"snake created at x={self.x} y={self.y}")

    def rotate_image_left(self):
        self.snake_image = self.snake_image.transformed(QTransform().rotate(-90))
        self.snake_label.setPixmap(self.snake_image)

    def rotate_image_right(self):
        self.snake_image = self.snake_image.transformed(QTransform().rotate(90))
        self.snake_label.setPixmap(self.snake_image)

    def mirror_image_horizontal(self):
        image = self.snake_image.toImage()
        mirrored_image = image.mirrored(False, True)
        self.snake_image = QPixmap.fromImage(mirrored_image)
        self.snake_label.setPixmap(self.snake_image)

    def mirror_image_vertical(self):
        image = self.snake_image.toImage()
        mirrored_image = image.mirrored(True, False)
        self.snake_image = QPixmap.fromImage(mirrored_image)
        self.snake_label.setPixmap(self.snake_image)

    def go_ahead(self):
        """
        Permet de faire avancer le serpent d'une case vers la direction dans laquelle il est tourné.
        """
        if self.is_alive and not self.has_reached_destination:
            self.movement_count += 1
            match self.current_direction:
                case 'right':
                    if self.x == 10 or self.game.blocks[self.y][self.x + 1].is_removed:
                        self.is_alive = False
                    if self.game.blocks[self.y][self.x + 1].passage_to_win > 0:
                        self.game.blocks[self.y][self.x + 1].passage_to_win -= 1
                        self.has_reached_destination = True
                        self.game.editor.animation_thread.animation_speed = ENDING_ANIMATION_SPEED
                        self.game.editor.animation_thread.animation_speed = ENDING_ANIMATION_SPEED
                    self.x += 1
                    self.mirror_image_horizontal()

                case 'top':
                    if self.y == 0 or self.game.blocks[self.y - 1][self.x].is_removed:
                        self.is_alive = False
                    if self.game.blocks[self.y - 1][self.x].passage_to_win > 0:
                        self.game.blocks[self.y - 1][self.x + 1].passage_to_win -= 1
                        self.has_reached_destination = True
                        self.game.editor.animation_thread.animation_speed = ENDING_ANIMATION_SPEED

                    self.y -= 1
                    self.mirror_image_vertical()

                case 'left':
                    if self.x == 0 or self.game.blocks[self.y][self.x - 1].is_removed:
                        self.is_alive = False
                    if self.game.blocks[self.y][self.x - 1].passage_to_win > 0:
                        self.game.blocks[self.y][self.x - 1].passage_to_win -= 1
                        self.has_reached_destination = True
                        self.game.editor.animation_thread.animation_speed = ENDING_ANIMATION_SPEED

                    self.x -= 1
                    self.mirror_image_horizontal()

                case 'bottom':
                    if self.y == 8 or self.game.blocks[self.y + 1][self.x].is_removed:
                        self.is_alive = False
                    if self.game.blocks[self.y + 1][self.x].passage_to_win > 0:
                        self.game.blocks[self.y + 1][self.x].passage_to_win -= 1
                        self.has_reached_destination = True
                        self.game.editor.animation_thread.animation_speed = ENDING_ANIMATION_SPEED

                    self.y += 1
                    self.mirror_image_vertical()

            self.game.board_layout.removeWidget(self.snake_label)
            self.game.board_layout.addWidget(self.snake_label, self.y, self.x)

            # verification sur le block sur lequel est placé le snake (est-ce qu'il a le droit d'etre sur ce block) :
            # if self.game.current_level.contraint(self.game.blocks[self.y][self.x]):
            #     pass

        if not self.is_alive:
            self.snake_label.setPixmap(self.snake_image_dead)
        self.movement_count += 1

    def turn_left(self):
        """
        Permet de faire changer la direction de l'image du serpent à gauche.
        """
        match self.current_direction:
            case 'right':
                self.current_direction = 'top'
            case 'top':
                self.current_direction = 'left'
            case 'left':
                self.current_direction = 'bottom'
            case 'bottom':
                self.current_direction = 'right'
        self.rotate_image_left()
        self.movement_count += 1

    def turn_right(self):
        """
        Permet de faire changer la direction de l'image du serpent à droite.
        """
        match self.current_direction:
            case 'right':
                self.current_direction = 'bottom'
            case 'top':
                self.current_direction = 'right'
            case 'left':
                self.current_direction = 'top'
            case 'bottom':
                self.current_direction = 'left'
        self.rotate_image_right()
        self.movement_count += 1

    def go_behind(self):
        """
        Permet de faire changer la direction de l'image du serpent à derrière.
        """
        self.turn_left()
        self.turn_left()
        self.movement_count -= 1  # mouvements deja comptés 2x avec turn_left
