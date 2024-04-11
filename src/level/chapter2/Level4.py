from src.level.Level import Level
from src.code_process.CodeParser import CodeParser
from config.config import VALID_CODE_MESSAGE, VALID_OUTPUT_MESSAGE, INVALID_OUTPUT_MESSAGE


class Level4(Level):

    def __init__(self, game):
        super().__init__(game)

        self.possible_solution = ("# Voici une solution possible pour ce niveau :\n"
                                  "print(4.4)")

        self.constraint_text = ("Affichez un réel qui n'est pas un entier en console\n"
                                "*sans utiliser de guillemets")

    def validate_output(self, output):
        if output != "":
            lines = output.splitlines()
            if lines != []:
                try:
                    float(lines[0].strip())
                    return VALID_OUTPUT_MESSAGE
                except ValueError:
                    pass
        return INVALID_OUTPUT_MESSAGE

    def validate_code(self, code):
        if code != "":
            if CodeParser.contains_string(code):
                return "Vous n'avez pas le droit d'utiliser de guillemets."

            elif CodeParser.contains_variable_manipulation(code):
                params = CodeParser.extract_param_in_function(code, "self.assignment")

                if not params == []:
                    for param in params:
                        message = VALID_CODE_MESSAGE
                        split_params = param.split(",")
                        for split_param in split_params:
                            try:
                                float_value = float(split_param)
                                if float_value == int(float_value):
                                    message = f"Code refusé car {float_value} est un entier."
                            except ValueError:
                                pass
                        return message
                    return "Vous n'avez pas utilisé de nombre réel."

            else:
                params = CodeParser.extract_param_in_function(code, "print")

                if params != []:
                    for param in params:
                        try:
                            float_value = float(param)
                            if float_value != int(float_value):
                                return VALID_CODE_MESSAGE
                            return f"Code refusé car {float_value} est un entier."
                        except ValueError:
                            pass
                    return "Vous n'avez pas utilisé de nombre réel."
                else:
                    return "Vous n'avez pas utilisé d'instruction print()."

        return "Pas de code !"
