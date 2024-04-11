FRAMELESS_HINT = False

SCREEN_LENGTH = 1280 - 64
SCREEN_HEIGHT = 720 - 110

ROW = 9
COL = 11

SLIDER_DIMENSION = [300, 65]

ENDING_ANIMATION_SPEED = 3

# Timer en ms avant que l'exécution du code s'arrête (anti boucle infini)
EXEC_TIMEOUT = 3000

# Timer avant de réactiver le bouton reset après avoir reset (le temps que l'animation précédente se termine)
RESET_TIMER = 1200

MAX_AMOUNT_CHAPTERS = 12

# Il est possible d'ajouter des chapitres ici, l'affichage se fera automatiquement
# {"titre du chapitre" : (indice premier niveau, indice dernier niveau)
CHAPTERS = [{"Hello World (1-2)": (1, 2)},
            {"Types et opérations (3-12)": (3, 12)},
            {"(Tutoriel) Terrain de jeu (13-16)": (13, 16)},
            {"Variables (17-18)": (17, 18)},
            {"Boucles (19-20)": (19, 20)},
            # Boucles
            ]

# Il est possible d'ajouter des valeurs à cette liste pour ajouter des boutons
# L'affichage se fera correctement automatiquement
LEFT_BUTTONS_TEXT = ['Accélérer', 'Ralentir', 'Aide', 'Solution', 'Clear', 'Menu']

VALID_CODE_MESSAGE = ""
INVALID_CODE_MESSAGE = "Votre code contient des instructions non autorisées pour ce niveau !"
VALID_OUTPUT_MESSAGE = ">> Résultat validé !"
INVALID_OUTPUT_MESSAGE = ">> Résultat incorrect !"


# Message affiché sur les niveaux qui ne possèdent pas de terrain de jeu
NO_BOARD_MESSAGE = ("Ce niveau ne contient pas de terrain de jeu !\n"
                    "Vous aurez uniquement besoin de l'éditeur python pour le faire.")
