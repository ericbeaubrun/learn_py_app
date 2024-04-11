from src.Snake import Snake
from src.level.Level import Level


class Level13(Level):

    def __init__(self, game):
        super().__init__(game)

        game.add_spawn_block(4, 0)
        game.add_block(4, 1)
        game.add_destination_block(4, 2)

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "print(\"avance\")\n"
                                  "print(\"avance\")")

        self.constraint_text = "Atteignez la case verte !"
        self.help_text = ("Avancez avec l'instruction:\n"
                          "print(\"avance\")")
