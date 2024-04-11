import logging

LOGGING_LEVEL = logging.INFO

# Chemin du fichier log
LOG_FILE_PATH = 'logs\logging.log'

# Permet d'activer l'affichage les logs en console
CONSOLE_LOGGING = True

# Permet d'activer la génération de fichier log
FILE_LOGGING = True

if FILE_LOGGING:
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=LOG_FILE_PATH, filemode='w', format=LOG_FORMAT, level=LOGGING_LEVEL)

if CONSOLE_LOGGING:
    LOG_CONSOLE_FORMAT = logging.Formatter('%(levelname)s - %(message)s')
    console_stream_handler = logging.StreamHandler()
    console_stream_handler.setLevel(LOGGING_LEVEL)
    console_stream_handler.setFormatter(LOG_CONSOLE_FORMAT)
    logging.getLogger('').addHandler(console_stream_handler)
