from src.code_process.CodeParser import CodeParser
from src.code_process.CodeRemover import CodeRemover
from src.code_process.CodeUtility import CodeUtility
from src.level.Level import Level
from config.config import VALID_CODE_MESSAGE, VALID_OUTPUT_MESSAGE, INVALID_OUTPUT_MESSAGE


class Level11(Level):
    def __init__(self, game):
        super().__init__(game)

        self.constraint_text = ("Prenons l'instruction python suivante : print(int(20/3))\n"
                                "Faites la même chose en utilisant la division entière \"//\"\n"
                                "*Vous n'avez pas le droit d'utiliser de cast : int()")

        self.possible_solution = ("print(20//3)")
        self.help_text = ("")

    def validate_output(self, output):
        lines = output.splitlines()
        if lines != []:
            if lines[0] == "6":
                return VALID_OUTPUT_MESSAGE
        return INVALID_OUTPUT_MESSAGE

    def validate_code(self, code: str):
        if code != "":
            code = CodeRemover.remove_comments(code)
            if "int()" in code:
                return "Vous n'avez pas le droit d'utiliser \"int()\""
            if not "//" in code:
                return "Vous n'avez pas utilisé la division entière \"//\""

            var_values = CodeParser.extract_variables_values(code)
            for val in var_values:
                val = CodeUtility.remove_quotes(val)
                try:
                    if int(val) == 6:
                        return "Vous n'avez pas le droit de définir une variable ayant pour valeur \"6\"."
                except ValueError:
                    pass

            params = CodeParser.extract_param_in_function(code, "print")
            for param in params:
                try:
                    if int(param.strip()) == 6:
                        return "Vous n'avez pas le droit d'afficher directement le résultat."
                except ValueError:
                    pass

            return VALID_CODE_MESSAGE
        return "Pas de code !"
