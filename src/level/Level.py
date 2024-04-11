from config.config import VALID_CODE_MESSAGE, VALID_OUTPUT_MESSAGE


class Level:
    """
    Cette classe permet de définir abstraitement tous les niveaux du jeu.
    Il s'agit de la classe mère des tous les niveaux.
    """

    def __init__(self, game):
        assert (game is not None)
        self.possible_solution = "# Navré, nous n'avons pas encore mis de solution pour ce niveau."
        self.constraint_text = "Pas d'énoncé pour ce niveau."
        self.help_text = "Pas d'aide pour ce niveau."
        self.is_no_blocks_level = False

    def validate_output(self, output):
        """
        Permet de vérifier que le texte en console est correct pour réussir le niveau.
        :param output: Le texte en console.
        :return: la chaine de caractère VALID_OUTPUT_MESSAGE si le texte en console est correct par rapport à l'énoncé.
        """
        return VALID_OUTPUT_MESSAGE

    def validate_code(self, code):
        """
        Permet de vérifier que le code est correct pour réussir le niveau.
        :param code: Code écrit par l'utilisateur.
        :return: la chaine de caractère VALID_CODE_MESSAGE si le code écrit par l'utilisateur est correct par rapport à l'énoncé.
        """
        return VALID_CODE_MESSAGE

    def get_prohibited_instructions(self):
        return None
