from config.config import VALID_CODE_MESSAGE
from src.level.Level import Level


class Level8(Level):
    def __init__(self, game):
        super().__init__(game)

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "print(1+1)\n"
                                  "print(7-4)\n"
                                  "print(2*2)\n"
                                  "print(15/3)")
        self.constraint_text = (
            "Utilisez de la manière que vous souhaitez l'addition, la soustration, la multiplication et la division.")

        # self.help_text = ("")

    def validate_code(self, code):
        if code != "":
            tmp_code = ""
            for line in code.splitlines():
                if not line.startswith("#"):
                    tmp_code += line
            if '+' in tmp_code and '-' in tmp_code and '*' in tmp_code and '/' in tmp_code:
                return VALID_CODE_MESSAGE
            return "Vous n'avez pas utilisé toutes les opérations."
        return "Pas de code !"
