from config.config import VALID_CODE_MESSAGE
from src.Snake import Snake
from src.code_process.CodeParser import CodeParser
from src.code_process.CodeRemover import CodeRemover
from src.level.Level import Level


class Level17(Level):

    def __init__(self, game):
        super().__init__(game)

        game.add_variable_block(4, 5, "var", None)

        self.possible_solution = "# Voici une solution possible pour ce niveau :"
        self.constraint_text = "Déclarez une variable qui s'appel var"
        self.help_text = "Pas d'aide pour ce niveau."

    def validate_code(self, code):
        if code != "":
            code = CodeRemover.remove_comments(code)
            if CodeParser.contains_variable_declaration(code, "var"):
                return VALID_CODE_MESSAGE
            return "La variable n'est pas correctement déclarée."
        return "Pas de code !"
