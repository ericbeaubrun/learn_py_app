from config.config import VALID_CODE_MESSAGE
from src.Snake import Snake
from src.code_process.CodeRemover import CodeRemover
from src.level.Level import Level


class Level19(Level):

    def __init__(self, game):
        super().__init__(game)

        game.add_spawn_block(4, 0)

        for i in range(1, 10):
            game.add_block(4, i)

        game.add_destination_block(4, 10)

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "for i in range(10):\n"                                  
                                  "\tprint(\"avance\")")

        self.constraint_text = "*Vous avez le droit d'utiliser uniquement une seule instruction pour avancer."

    def validate_code(self, code):
        if code != "":
            code = CodeRemover.remove_comments(code)
            if code.count('forward_animation') > 1:
                return "Vous n'avez pas le droit d'utiliser plusieurs instructions pour avancer."
            return VALID_CODE_MESSAGE
        return "Pas de code !"
