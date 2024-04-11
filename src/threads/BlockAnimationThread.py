from PyQt6.QtCore import pyqtSignal, QThread

from logs.LogsConfig import *


class BlockAnimationThread(QThread):
    """
    Cette classe permet d'animer un Block. (Cette classe n'a pas été utilisée finalement)
    """

    signal = pyqtSignal()

    def __init__(self, game):
        if FILE_LOGGING:
            logging.basicConfig(format=LOG_FORMAT, level=LOGGING_LEVEL)
        super().__init__()
        self.game = game
        self.isRunning = True

    def connect_blocks(self):
        for block in self.game.changing_variable_blocks:
            print("connection")
            self.signal.connect(block.next_changing_value)

    def disconnect_all(self):
        self.signal.disconnect()

    def stop(self):
        self.disconnect_all()
        # self.disconnect()
        self.isRunning = False

    def run(self):
        while self.isRunning:
            print(f"REF = {self.__str__()}")

            try:
                self.signal.emit()
                print("// EMIT //")
                QThread.msleep(self.game.editor.animation_thread.animation_speed)

            except Exception as e:
                self.stop()
                print(f"Une erreur d'animation d'un block est survenu : {e}")
