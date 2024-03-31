from PyQt5 import QtCore

from app.utils.logger import get_logger

logger = get_logger(__name__)


class KeyStrokes:
    def __init__(self, callback):
        self.content = ''
        self.callback = callback
        self.waiting_for_input = True

    def reset(self):
        self.waiting_for_input = True
        self.content = ''

    def check_for_event(self):
        if self.waiting_for_input:
            QtCore.QTimer.singleShot(1000, lambda: self.check_for_event())
        else:
            QtCore.QTimer.singleShot(100, lambda: self.callback(self.content))

    def handle_event(self, event):
        try:
            print(str(chr(event.key())))
        except Exception:
            print(event.key())

        if event.key() == 16777248:  # Weird thing
            return

        try:
            self.content += chr(event.key())
        except Exception:
            logger.info("Keystrokes:" + str(self.content))
            self.waiting_for_input = False
