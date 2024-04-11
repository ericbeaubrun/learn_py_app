import re

from logs.LogsConfig import *


class CodeRemover:
    """
    Cette classe permet d'utiliser des méthodes qui permettent de retirer des instructions ou des partie de code dans un code python.
    """

    COMMENT_REGEX = r"#.*"

    PARENTHESES_REGEX = r"\((\w+)\)"

    if FILE_LOGGING:
        logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

    @staticmethod
    def remove_unnecessary_blank_lines(code):
        """
        Cette méthode permet de retirer les lignes vides inutiles dans le code donné en parametre.
        :param code : Chaine de caractère représentant le code python.
        :return : Le code python sans les lignes vides inutiles.
        """
        assert isinstance(code, str)
        lines = code.splitlines()
        result = '\n'.join([line for line in lines if line.strip() != ''])

        return result

    @staticmethod
    def remove_comments(code):
        """
        Cette méthode permet de retirer les commentaires dans un code python.
        :param code: Chaine de caractère représentant le code python.
        :return : Le code python sans les commentaires.
        """
        uncommented_code = re.sub(CodeRemover.COMMENT_REGEX, "", code)
        lines = uncommented_code.split('\n')
        result_lines = [ligne for ligne in lines if ligne.strip() != ""]
        indented_uncommented_code = '\n'.join(result_lines)

        return indented_uncommented_code

    @staticmethod
    def balanced_parentheses(expression):
        balance = 0
        for c in expression:
            if c == '(':
                balance += 1
            elif c == ')':
                balance -= 1
            if balance < 0:
                return False
        return balance == 0

    @staticmethod
    def remove_unnecessary_parentheses(expression):
        """
        Cette méthode permet de retirer les parentheses inutiles dans le code donné en parametre.
        :param code : Chaine de caractère représentant le code python.
        :return : Le code python sans les parentheses inutiles.
        """

        while re.search(CodeRemover.PARENTHESES_REGEX, expression):
            # r'\1' pour le deuxieme arg d'expression
            expression = re.sub(CodeRemover.PARENTHESES_REGEX, r'\1', expression)

        while (expression.startswith('(') and expression.endswith(')') and
               CodeRemover.balanced_parentheses(expression[1:-1])):
            expression = expression[1:-1]

        return expression
