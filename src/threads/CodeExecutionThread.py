import sys
from io import StringIO

from PyQt6.QtCore import QThread, pyqtSignal
from logs.LogsConfig import *


class CodeExecutionThread(QThread):
    """
    Cette classe permet de faire une première exécution pour test le code non formaté de l'utilisateur
    pour voir s'il y a des erreurs de synthaxe et/ou boucle infinie.
    """

    # Permet d'arrêter l'exécution du thread.
    terminate_signal = pyqtSignal(object)

    def __init__(self):
        super(CodeExecutionThread, self).__init__()
        if FILE_LOGGING:
            logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

        self.code = ""
        self.captured_output = ""

    def run(self):
        logging.info(f"the following user code attempts to be executed :\n{self.code}")
        try:
            # Redirige la sortie standard pour la stocker dans captured_output
            output_buffer = StringIO()
            original_stdout = sys.stdout
            sys.stdout = output_buffer

            exec(self.code)

            sys.stdout = original_stdout
            self.captured_output = output_buffer.getvalue()

            # Emet le signal avec None pour signaler qu'il n'y a pas eu d'erreur
            self.terminate_signal.emit(None)
        except Exception as e:
            # Emet le signal avec l'exception (erreur détéctée dans le code de l'utilisateur)
            self.terminate_signal.emit(e)
