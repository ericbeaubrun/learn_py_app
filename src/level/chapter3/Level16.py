from src.Snake import Snake
from src.level.Level import Level


class Level16(Level):

    def __init__(self, game):
        super().__init__(game)

        self.possible_solution = "# Voici une solution possible pour ce niveau :"

        self.constraint_text = "CE NIVEAU N'EST PAS FAIT"
        self.help_text = "Pas d'aide pour ce niveau."
