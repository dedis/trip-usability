from PyQt5 import QtWidgets, QtCore

from app.utils.logger import get_logger

logger = get_logger(__name__)


class QtButton(QtWidgets.QPushButton):
    def __init__(self, parent, config, lang, QRectCoordinates, callback):
        super(QtButton, self).__init__(parent)
        self.setGeometry(QRectCoordinates)
        self.config = config
        self.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.setDefault(False)
        self.setObjectName("Button")
        self.setDisabled(True)

        timeout = int(self.config.button_timeout) if not hasattr(lang, "B_Hidden") else lang.B_Hidden
        QtCore.QTimer.singleShot(timeout, lambda: self.setEnabled(True))

        self.clicked.connect(callback)
        if hasattr(lang, "Callback_After"):
            self.setHidden(True)
            QtCore.QTimer.singleShot(lang.Callback_After, lambda: callback())
