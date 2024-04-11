from src.code_process.CodeRemover import CodeRemover
from src.code_process.CodeUtility import CodeUtility
from src.code_process.CodeParser import CodeParser
from config.config import VALID_OUTPUT_MESSAGE, INVALID_OUTPUT_MESSAGE, VALID_CODE_MESSAGE
from src.level.Level import Level


class Level10(Level):
    def __init__(self, game):
        super().__init__(game)

        self.constraint_text = ("\"tic\" et \"tac\" sont deux chaines de caractère.\n"
                                "Utilisez les pour former la chaine de caractère \"tictac\" et affichez le résultat.\n"
                                "*Vous n'avez pas le droit d'utiliser la chaine \"tictac\".\n")
        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "print(\"tic\"+\"tac\")")
        # self.help_text = ("")

    def validate_output(self, output):
        if output != "":
            lines = output.splitlines()
            if lines != [] and (lines[0].strip() == "tictac"):
                return VALID_OUTPUT_MESSAGE
        return INVALID_OUTPUT_MESSAGE

    def validate_code(self, code):
        if code != "":
            code = CodeRemover.remove_comments(code)

            if (not "tic" in code) or (not "tac" in code):
                return "Vous devez utiliser les deux valeurs suivantes : \"tic\" et \"tac\""

            lines = code.splitlines()

            for line in lines:
                print("line =" + line)
                if (((line.strip().startswith('print') and '"' in line
                      or line.strip().startswith('print') and "'" in line)
                     and "tictac" in line)):
                    return "Vous n'avez pas le droit d'utiliser la chaine \"tictac\"."

            var_values = CodeParser.extract_variables_values(code)
            for val in var_values:
                val = CodeUtility.remove_quotes(val)
                if val.strip() == 'tictac':
                    return "Vous n'avez pas le droit de définir une variable ayant pour valeur \"tictac\""

            return VALID_CODE_MESSAGE
        return "Pas de code !"
