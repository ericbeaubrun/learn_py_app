from config.config import VALID_OUTPUT_MESSAGE, INVALID_OUTPUT_MESSAGE, VALID_CODE_MESSAGE
from src.level.Level import Level
from src.code_process.CodeParser import CodeParser
from src.code_process.CodeRemover import CodeRemover


class Level7(Level):
    VALUE = 5.43219876

    def __init__(self, game):
        super().__init__(game)

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n" +
                                  "print(len(str(" + str(self.VALUE) + ")))")
        self.constraint_text = (str(self.VALUE) + " est un réel.\n"
                                                  "Affichez le nombre de caractères présents dans cette valeur.\n"
                                                  "(le résultat attendu est un nombre entier)\n"
                                                  "*sans utiliser d'entier dans votre programme\n"
                                                  "*sans utiliser de guillemets")
        self.help_text = "Utilisez la fonction len()."

    def validate_output(self, output):
        if output != "":
            lines = output.splitlines()
            if lines != [] and lines[0].strip() == str(len(str(self.VALUE))):
                return VALID_OUTPUT_MESSAGE
        return INVALID_OUTPUT_MESSAGE

    def validate_code(self, code):
        if code != "":

            code = CodeRemover.remove_comments(code)

            if CodeParser.contains_value(code, int(self.VALUE)):
                return "Vous n'avez pas utilisé la valeur " + str(self.VALUE) + "."

            # lines = code.splitlines()
            # i = 0
            # size = len(lines) - 1
            # for line in lines:
            #     if str(self.VALUE) in line:
            #         break
            #     if i == size:
            #         return "Vous n'avez pas utilisé la valeur " + str(self.VALUE) + "."
            #     i += 1

            if CodeParser.contains_string(code):
                return "Vous n'avez pas le droit d'utiliser de guillemets."

            if CodeParser.contains_integer(code):
                return "Vous n'avez pas le droit d'utiliser d'entier."
            return VALID_CODE_MESSAGE
        return "Pas de code !"
