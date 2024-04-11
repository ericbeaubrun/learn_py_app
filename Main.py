import traceback

from PyQt6.QtWidgets import QApplication

from logs.LogsConfig import *
from src.MainWindow import MainWindow

if FILE_LOGGING:
    logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)

app = QApplication([])
app.setStyleSheet(open("styles/stylesheet.css", "r").read())

try:
    main_window = MainWindow()
    main_window.show()
    app.exec()

except Exception as e:
    traceback.print_exc()
    logging.fatal(f"FATAL ERREUR : {e}")
