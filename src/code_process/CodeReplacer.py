import re

from logs.LogsConfig import *


class CodeReplacer:
    # pattern (regex) de tous les assignements de variable (par exemple ma_variable1 = 50)
    ASSIGNMENT_REGEX = r"^(?:(\t+))?([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$"

    # pattern (regex) de toutes les operation de variable (par exemple ma_variable2 += 1)
    OPERATION_REGEX = r"^(?:(\t+))?([a-zA-Z_][a-zA-Z0-9_]*)\s*([\+\-\*/%]=)\s*(.+)$"

    # operateurs standars en python
    OPERATORS = {'+=': '+', '-=': '-', '*=': '*', '/=': '/', '//=': '//', '%=': '%'}

    # pattern (regex) des définitions de fonctions
    FUNCTION_DEFINITION_REGEX = r"def (\w+)\((.*?)\):"

    if FILE_LOGGING:
        logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

    @staticmethod
    def replace_assignments(code):
        """
        Permet de remplacer les instructions d'assignements pour qu'elles puissent intéragir avec le terrain de jeu.
        :param code: Un code python.
        :return: le code python avec les instructions qui intéragissent avec le terrain.
        """
        assert (isinstance(code, str))

        def replacement(match):
            tabs = match.group(1) or ""
            variable_name = match.group(2).rstrip("\r\n")
            value = match.group(3).rstrip('\r\n')
            modified = f"{tabs}self.assignment('{variable_name}', {value})"
            original_with_tabs = f"{tabs}{variable_name} = {value}"
            return original_with_tabs + "\n" + modified

        return re.sub(CodeReplacer.ASSIGNMENT_REGEX, replacement, code, flags=re.MULTILINE)

    @staticmethod
    def replace_operations(code):
        """
        Permet de remplacer les instructions d'assignements avec opérations pour qu'elles puissent intéragir avec le terrain de jeu.
        :param code: Un code python.
        :return: le code python avec les instructions d'opérations qui intéragissent avec le terrain.
        """
        assert (isinstance(code, str))

        # Fonction imbriquée pour eviter les fonction non utilisable dans CodeReplacer
        def replacement(match):
            tabs = match.group(1) or ""
            variable_name = match.group(2).rstrip('\r\n')
            code_operator = match.group(3)
            value = match.group(4).rstrip('\r\n')

            operator = CodeReplacer.OPERATORS[code_operator]
            modified = f"{tabs}self.assignment('{variable_name}', {variable_name} {operator} {value})"
            original_with_tabs = f"{tabs}{variable_name} {code_operator} {value}"

            return modified + "\n" + original_with_tabs

        return re.sub(CodeReplacer.OPERATION_REGEX, replacement, code, flags=re.MULTILINE)

    @staticmethod
    def add_self_to_functions(code):
        """
        Ajoute self devant les déclaration de fonction d'un code python.
        :param code: Un code python.
        :return: Le code python avec les déclaration de fonction qui ont self en premeir argument.
        """
        assert (isinstance(code, str))

        # Fonction imbriquée pour eviter les fonction non utilisable dans CodeReplacer
        def replacement(match):
            function_name = match.group(1)
            parameters = match.group(2)
            if parameters:
                return f"def {function_name}(self, {parameters}):"
            else:
                return f"def {function_name}(self):"

        return re.sub(CodeReplacer.FUNCTION_DEFINITION_REGEX, replacement, code)
