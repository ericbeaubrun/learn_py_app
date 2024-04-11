from src.level.Level import Level
from config.config import VALID_CODE_MESSAGE, VALID_OUTPUT_MESSAGE, INVALID_OUTPUT_MESSAGE
from src.code_process.CodeParser import CodeParser


class Level3(Level):

    def __init__(self, game):
        super().__init__(game)

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "print(5)")

        self.constraint_text = ("Affichez un entier en console\n"
                                "*sans utiliser de guillemets")

    def validate_output(self, output):
        if output != "":
            lines = output.splitlines()
            if lines != []:
                try:
                    int(lines[0].strip())
                    return VALID_OUTPUT_MESSAGE
                except ValueError:
                    pass
        return INVALID_OUTPUT_MESSAGE

    def validate_code(self, code):
        if code != "":
            if CodeParser.contains_string(code):
                return "Vous n'avez pas le droit d'utiliser de guillemets."
            return VALID_CODE_MESSAGE
        return "Pas de code!"
