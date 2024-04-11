from config.config import VALID_CODE_MESSAGE, VALID_OUTPUT_MESSAGE, INVALID_OUTPUT_MESSAGE
from src.level.Level import Level
import re
from src.code_process.CodeParser import CodeParser
from src.code_process.CodeRemover import CodeRemover


class Level9(Level):
    def __init__(self, game):
        super().__init__(game)

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "print(1/(1/2))")
        self.constraint_text = ("Effectuez l'opération : 1 divisé par un demi.\n"
                                "(directement dans print()) \n"
                                "(sans utiliser de guillemets)\n")

        self.help_text = ("Utilisez des parenthèses.")

    def validate_output(self, output):
        if output != "":
            lines = output.splitlines()
            if lines != [] and (lines[0].strip() == "2.0" or lines[0].strip() == "2"):
                return VALID_OUTPUT_MESSAGE
        return INVALID_OUTPUT_MESSAGE

    def validate_code(self, code):
        if code != "":
            if CodeParser.contains_string(code):
                return "Vous n'avez pas le droit d'utiliser de guillemets"

            code = CodeRemover.remove_comments(code)

            params = CodeParser.extract_param_in_function(code, "print")
            for param in params:
                params_split = param.split(',')
                for param_split in params_split:
                    param_split = CodeRemover.remove_unnecessary_parentheses(param_split)
                    # L'expression régulière ci-dessous permet de retrouver toutes les expréssions égales à 1 / (1/2)
                    if re.match(r'^\s*1\s*\/\s*\(\s*1\s*\/\s*2\s*\)\s*$', param_split):
                        return VALID_CODE_MESSAGE
            return ("Code refusé car l'expression fournit n'est pas correcte, "
                    "où car il y a des parenthèses inutiles.")
        return "Pas de code !"
