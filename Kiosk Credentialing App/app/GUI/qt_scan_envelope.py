from importlib import resources

from PyQt5 import QtWidgets, QtCore, QtGui

from app.components.symbol import Symbol
from app.utils.lang import Lang


class QtScanEnvelope(QtWidgets.QFrame):
    def __init__(self, parent, config, participant, lang, printed_symbol):
        super(QtScanEnvelope, self).__init__(parent)
        self.setGeometry(QtCore.QRect(520, 140, 1400, 920))
        self.setObjectName("frame")
        self.config = config
        self.participant = participant
        self.lang = lang
        self.printed_symbol = printed_symbol

        self.Heading = QtWidgets.QLabel(self)
        self.Heading.setGeometry(QtCore.QRect(20, 20, 1360, 200))
        self.Heading.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.Heading.setAlignment(QtCore.Qt.AlignCenter)

        if self.participant.ab_malicious_kiosk:
            height = 160
        else:
            height = 240

        self.SubHeading = QtWidgets.QLabel(self)
        self.SubHeading.setGeometry(QtCore.QRect(20, height, 1360, 140))
        self.SubHeading.setStyleSheet("font: 48pt \"" + self.config.font + "\";")
        self.SubHeading.setAlignment(QtCore.Qt.AlignCenter)

        self.EnvelopeImage = QtWidgets.QLabel(self)
        self.EnvelopeImage.setGeometry(QtCore.QRect(580, height + 160, 180, 510))
        with resources.path("app.resources.images", "envelope_" + str(printed_symbol) + ".png") as image_path:
            self.EnvelopeImage.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.EnvelopeImage.setScaledContents(True)

        self.ScannerImage = QtWidgets.QLabel(self)
        self.ScannerImage.setGeometry(QtCore.QRect(320, height + 160 + 40, 200, 200))
        with resources.path("app.resources.images", "scanner.png") as image_path:
            transform = QtGui.QTransform()
            transform.scale(-1, 1)
            self.ScannerImage.setPixmap(QtGui.QPixmap(str(image_path.absolute())).transformed(transform))
        self.ScannerImage.setScaledContents(True)

        self.re_translate_ui()

    def re_translate_ui(self):
        self.Heading.setText(Lang.filter(self.lang.Heading, self.participant))
        symbol_text = "<span style=\"font-weight:550\">" + self.printed_symbol[0].upper() + self.printed_symbol[1:] + \
                      "</span> (" + Symbol.get_unicode_symbol(self.printed_symbol) + ")"
        self.SubHeading.setText(Lang.filter(self.lang.SubHeading, self.participant).replace('?', symbol_text))
