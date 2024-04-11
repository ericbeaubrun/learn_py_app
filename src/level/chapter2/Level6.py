from src.level.Level import Level
from src.code_process.CodeParser import CodeParser
from config.config import VALID_CODE_MESSAGE, VALID_OUTPUT_MESSAGE, INVALID_OUTPUT_MESSAGE


class Level6(Level):
    VALUE = "2.5"

    def __init__(self, game):
        super().__init__(game)

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "print(int(float(\"" + self.VALUE + "\")))")
        self.constraint_text = ("\"" + self.VALUE + "\" est une chaine de caractère.\n"
                                                    "Utilisez la pour afficher sa valeur entière en console\n"
                                                    "*sans faire d'opérations\n"
                                                    "*sans utiliser de guillemets sauf pour : \"" + self.VALUE + "\"")

        # self.help_text = ("")

    def validate_output(self, output):
        if output != "":
            lines = output.splitlines()
            if lines != [] and lines[0].strip() == str(int(float(self.VALUE))):
                return VALID_OUTPUT_MESSAGE
        return INVALID_OUTPUT_MESSAGE

    def validate_code(self, code):
        if code != "":

            lines = code.splitlines()

            params = CodeParser.extract_param_in_function(code, "print")
            for param in params:
                if ("-" in param or "+" in param or "*" in param or "/" in param
                        or (str(int(float(self.VALUE))) in param and not self.VALUE in param)):
                    return (
                            "Code refusé car vous n'utilisez pas la chaine de caractère \"" + self.VALUE + "\" ou car vous utilisez "
                                                                                                           "une/des opération(s).")
            # Vérifier que l'utilisateur n'utilise pas de guillements sauf pour 2.5
            for line in lines:
                if (((line.strip().startswith('print') and '"' in line
                      or not line.strip().startswith('#') and '"' in line)
                     or line.strip().startswith('print') and "'" in line
                     or not line.strip().startswith('#') and "'" in line)
                        and not self.VALUE in line):
                    return "Vous n'avez pas le droit d'utiliser de guillemets."
            return VALID_CODE_MESSAGE
        return "Pas de code !"
