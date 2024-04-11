from config.config import VALID_CODE_MESSAGE
from src.Snake import Snake
from src.code_process.CodeRemover import CodeRemover
from src.level.Level import Level


class Level20(Level):

    def __init__(self, game):
        super().__init__(game)

        game.add_spawn_block(0, 0)

        for i in range(0, 8):
            game.add_block(0, i + 1)

        for i in range(0, 7):
            game.add_block(i, 7 + 1)

        for i in range(7, 0, -1):
            game.add_block(7, i + 1)

        for i in range(6, 1, -1):
            game.add_block(i, 1 + 1)

        for i in range(2, 6):
            game.add_block(2, i + 1)

        for i in range(3, 5):
            game.add_block(i, 5 + 1)

        for i in range(5, 2, -1):
            game.add_block(5, i + 1)

        game.add_destination_block(4, 3 + 1)

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "for i in range(8):\n"
                                  "\tfor _ in range(8-i,0,-1):\n"
                                  "\t\tprint(\"avance\")\n"
                                  "\tprint(\"droite\")\n")

        self.constraint_text = "*Vous avez le droit d'utiliser uniquement une seule instruction pour avancer."

    def validate_code(self, code):
        if code != "":
            code = CodeRemover.remove_comments(code)
            if code.count('forward_animation') > 1:
                return "Vous n'avez pas le droit d'utiliser plusieurs instructions pour avancer."
            return VALID_CODE_MESSAGE
        return "Pas de code !"
