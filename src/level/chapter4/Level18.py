from config.config import VALID_CODE_MESSAGE
from src.Snake import Snake
from src.code_process.CodeRemover import CodeRemover
from src.level.Level import Level


class Level18(Level):

    def __init__(self, game):
        super().__init__(game)

        game.add_spawn_block(4, 0)

        game.add_variable_block(4, 1, "tmp", None)
        game.add_variable_block(3, 1, "val1", 5)
        game.add_variable_block(5, 1, "val2", 2)

        game.add_block(4, 2)

        self.possible_solution = "# Voici une solution possible pour ce niveau :"

        self.constraint_text = "Permutez deux variables (CE NIVEAU A ETE N'EST PAS FONCTIONNEL)"
        self.help_text = "Pas d'aide pour ce niveau."