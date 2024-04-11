from src.Snake import Snake
from src.level.Level import Level


class Level14(Level):

    def __init__(self, game):
        super().__init__(game)

        game.add_spawn_block(4, 0)
        game.add_block(4, 1)
        game.add_block(4, 2)
        game.add_block(5, 2)
        game.add_destination_block(6, 2)

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "print(\"avance\")\n"
                                  "print(\"avance\")\n"
                                  "print(\"droite\")\n"
                                  "print(\"avance\")\n"
                                  "print(\"avance\")")

        self.constraint_text = "Pas d'énoncé pour ce niveau."
        self.help_text = ("Changez de direction avec les intructions suivantes :\n"
                          "print(\"droite\")\n"
                          "print(\"gauche\")\n"
                          "print(\"derriere\")"
                          )
