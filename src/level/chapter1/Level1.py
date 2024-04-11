from src.level.Level import Level
from config.config import VALID_OUTPUT_MESSAGE, INVALID_OUTPUT_MESSAGE


class Level1(Level):

    def __init__(self, game):
        super().__init__(game)

        self.help_text = ("Pour afficher du texte en console utilisez l'instruction :\n"
                          "print(\"votre texte\")")

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "print(\"Hello World\")")

        self.constraint_text = "Affichez : Hello World"

    def validate_output(self, output):
        lines = output.splitlines()
        if lines != []:
            if lines[0] == "Hello World":
                return VALID_OUTPUT_MESSAGE

        return INVALID_OUTPUT_MESSAGE
