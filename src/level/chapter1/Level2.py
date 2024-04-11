from src.level.Level import Level
from config.config import VALID_CODE_MESSAGE


class Level2(Level):

    def __init__(self, game):
        super().__init__(game)

        self.help_text = "Pour commenter du code commencez une ligne avec #."

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "# Ceci est un commentaire de code")

        self.constraint_text = "Ecrivez un commentaire de code"

    def validate_code(self, code):
        if code != "":
            lines = code.splitlines()
            for line in lines:
                if line.strip().startswith('#'):
                    return VALID_CODE_MESSAGE
        return "Vous n'avez pas écris de commentaire de code."
