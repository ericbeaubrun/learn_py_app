import json

from logs.LogsConfig import *

# chemin vers le fichier qui garde en mémoire les indices des niveaux réussis
FILE_PATH = "src/level/levels_won.json"


class LevelWonSaver:
    """
    Cette classe permet de sauvegarder dans un fichier JSON les indices des niveaux qui ont été terminés par l'utilisateur.
    """
    if FILE_LOGGING:
        logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

    @staticmethod
    def save_list(level_index_list):
        try:
            file = open(FILE_PATH, "w")
            json.dump(level_index_list, file)
        except:
            logging.error(f"Incorrect file path to save won level index \"{FILE_PATH}\"")

    @staticmethod
    def read_list():
        try:
            file = open(FILE_PATH, "r")
            if file is not None:
                data = file.read()
                if not data:
                    return []
                return json.loads(data)
        except FileNotFoundError:
            logging.error(f"Incorrect file path to read won level index \"{FILE_PATH}\"")
            return []

    @staticmethod
    def append(level_index):
        liste = LevelWonSaver.read_list()
        liste.append(level_index)
        LevelWonSaver.save_list(liste)
