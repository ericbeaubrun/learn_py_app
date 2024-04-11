from src.Snake import Snake
from src.level.Level import Level


class Level15(Level):

    def __init__(self, game):
        super().__init__(game)

        game.add_spawn_block(4, 0)

        for i in range(1, 4):
            game.blocks[4][i].set_empty()
            game.add_block(4, i)

        for i in range(3, 8):
            game.add_block(3, i)
        for i in range(7, 10):
            game.add_block(4, i)

        game.add_block(5, 2)
        for i in range(2, 9):
            game.add_block(6, i)
        game.add_block(5, 8)

        game.add_destination_block(4, 10)

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "print(\"avance\")\n"
                                  "print(\"avance\")\n"
                                  "print(\"avance\")\n"
                                  "print(\"gauche\")\n"
                                  "print(\"avance\")\n"
                                  "print(\"droite\")\n"
                                  "print(\"avance\")\n"
                                  "print(\"avance\")\n"
                                  "print(\"avance\")\n"
                                  "print(\"avance\")\n"
                                  "print(\"droite\")\n"
                                  "print(\"avance\")\n"
                                  "print(\"gauche\")\n"
                                  "print(\"avance\")\n"
                                  "print(\"avance\")\n"
                                  "print(\"avance\")"
                                  )
        self.constraint_text = "Atteignez la case verte !"
