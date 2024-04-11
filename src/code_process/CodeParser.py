import re

from logs.LogsConfig import *
from src.code_process.CodeRemover import CodeRemover
from src.code_process.CodeUtility import CodeUtility


class CodeParser:
    """
    Cette classe permet de parcourir du code python pour savoir s'il contient certaines instructions ou récupérer certaines isntructions.
    """

    if FILE_LOGGING:
        logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

    @staticmethod
    def extract_param_in_function(code, function):
        """
        Récupère une liste de parametres présent dans une fonction donnée.
        :param code : Le code python à formatter de l'utilisteur.
        :param function : La fonction dont on veut extraire les parametres.
        :return : La liste de str représentant les parametres présent dans la fonction "function", retourne []
        s'il n'y en a pas.
        """
        assert (isinstance(code, str) and isinstance(function, str))

        result = []

        for line in code.splitlines():
            if line.strip().startswith(function + "(") and line.strip().endswith(")"):
                params_start = line.find('(') + 1
                params_end = line.rfind(')')
                params = line[params_start:params_end]
                result.append(params)

        return result

    @staticmethod
    def extract_variables_values(code):
        """
        Récupère les valeurs de tous les assignements de variable dans le code donné en parametre.
        Cette fonction en fonctionne que si le code python de l'utilisateur a été formaté.
        :param code : Le code python formaté de l'utilisateur.
        :return : Une liste str représentant les valeurs des variables assignées dans le code pris en parametre.
        """
        assert (isinstance(code, str))

        params = CodeParser.extract_param_in_function(code, "self.assignment")
        result = []
        for param in params:
            params_split = param.split(',')
            i = 0
            for param_split in params_split:
                if i > 0:
                    result.append(str(param_split))
                i += 1

        return result

    @staticmethod
    def contains_operations(code):
        """
        Vérifie si el code contient des opérations.
        :param code : Le code python de l'utilisateur.
        :return : True si le code contient des opérations, False sinon.
        """
        assert (isinstance(code, str))

        lines = code.splitlines()
        for line in lines:
            if ("-" in line or "+" in line or "*" in line or "/" in line
                    or "//" in line or "%" in line):
                return True
        return False

    @staticmethod
    def contains_value(code, integer_value):
        """
        Vérifie si le code donné en parametre contient une valeur donnée. Retourne True si la valeur est inclu, sinon retourne False.
        :param code : Le code python dont on doit vérifier si un entier est inclus dedans.
        :param integer_value : La valeur dont on doit vérifier si elle est inclu dans le code python ou non.
        """

        assert (isinstance(code, str))

        value = str(integer_value)
        lines = code.splitlines()
        i = 0
        size = len(lines) - 1
        for line in lines:
            if value in line:
                break
            if i == size:
                return True
            i += 1
        return False

    @staticmethod
    def contains_string(code):
        """
        Vérifie si le code contient des chaines de caractères.
        :param code : Le code dont on veut vérigier s'il contient des chaiens de caractères.
        """
        assert (isinstance(code, str))
        if code != "":
            lines = code.splitlines()
            for line in lines:
                if not line.strip().startswith('self.assignment'):
                    if ((line.strip().startswith('print') and '"' in line
                         or not line.strip().startswith('#') and '"' in line
                         or line.strip().startswith('print') and "'" in line)
                            or not line.strip().startswith('#') and "'" in line):
                        return True
        return False

    @staticmethod
    def contains_integer(code):
        """
        Vérifier si le code contient des entiers.
        :param code: Le code dont on veut vérifier s'il contient des entiers.
        :return: True si le code contient des entiers, False si le code n'en contient pas.
        """
        assert (isinstance(code, str))

        if code != "":
            lines = code.splitlines()
            for line in lines:
                if not line.strip().startswith('self.assignment') and not line.strip().startswith('#'):
                    for line_split in line.split():
                        if line_split.isdigit():
                            return True
                        try:
                            value = int(line_split)
                            if value == int(value):
                                return False
                        except ValueError:
                            pass

                elif line.strip().startswith('self.assignment'):
                    params = CodeParser.extract_param_in_function(code, 'self.assignment')
                    for param in params:
                        split_params = param.split(',')

                        for split_param in split_params:
                            try:
                                value = int(split_param)
                                if value == int(value):
                                    return False
                            except ValueError:
                                pass
        return False

    @staticmethod
    def contains_variable_manipulation(code):
        """
        Vérifie si le code python donné en parametre contient des manipulations de variables.
        :param code : Le code python dont on veut vérifier s'il contient des manipulations de variable.
        :return : True si le code contient des manipulations de variable, False sinon.
        """
        assert (isinstance(code, str))
        return "self.assignment" in code

    @staticmethod
    def contains_variable_declaration(code, name):
        """
        Vérifie si le code python donné en parametre contient des déclarations de variables.
        :param code : Le code python dont on veut vérifier s'il contient des déclarations de variable.
        :return : True si le code contient des déclarations de variable, False sinon.
        """
        assert (isinstance(code, str))
        code = CodeRemover.remove_comments(code)
        return f"self.assignment('{name}'" in code and not "None" in code
