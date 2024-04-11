from src.level.Level import Level
from src.code_process.CodeRemover import CodeRemover
from src.code_process.CodeParser import CodeParser
from config.config import VALID_CODE_MESSAGE, VALID_OUTPUT_MESSAGE, INVALID_OUTPUT_MESSAGE


class Level5(Level):
    VALUE = "1.618"

    def __init__(self, game):
        super().__init__(game)

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "print(int(" + self.VALUE + "))")
        self.constraint_text = (
                self.VALUE + " est un réel.\n"
                             "Utilisez le pour afficher sa valeur entière en console.\n"
                             "*sans faire d'opérations\n"
                             "*sans utiliser de guillemets")
        self.help_text = ("Utilisez int().")

    def validate_output(self, output):
        if output != "":
            lines = output.splitlines()
            if lines != [] and lines[0].strip() == "1":
                return VALID_OUTPUT_MESSAGE
        return INVALID_OUTPUT_MESSAGE

    def validate_code(self, code):
        if code != "":
            code = CodeRemover.remove_comments(code)

            if CodeParser.contains_operations(code):
                return "Code refusé car vous utilisez une/des opération(s)."

            params = CodeParser.extract_param_in_function(code, "print")
            for param in params:
                if ("-" in param or "+" in param or "*" in param or "/" in param
                        or "//" in param or "%" in param
                        or ("1" in param and not self.VALUE in param)):
                    return "Code refusé car vous n'utilisez pas la valeur " + self.VALUE + "."

            if CodeParser.contains_string(code):
                return "Vous n'avez pas le droit d'utiliser de guillemets."
            return VALID_CODE_MESSAGE
        return "Pas de code !"

