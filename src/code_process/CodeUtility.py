from logs.LogsConfig import *


class CodeUtility:
    """
    Cette classe contient les méthodes pour mannipuler des chaines de caractères.
    """
    if FILE_LOGGING:
        logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

    @staticmethod
    def remove_quotes(s):
        """
        Retire les guillements dans une chaine de caractère.
        :param s: une chaine de caractères
        :return: la chaine de caractère sans les guillements
        """
        s = s.strip()
        if s.startswith('"') and s.endswith('"') or s.startswith("'") and s.endswith("'"):
            s = s[1:-1]
        return s
