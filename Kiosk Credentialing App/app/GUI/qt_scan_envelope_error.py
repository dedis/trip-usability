from PyQt5 import QtWidgets, QtCore

from app.components.symbol import Symbol
from app.utils.lang import Lang


class QtScanEnvelopeError(QtWidgets.QFrame):
    def __init__(self, parent, config, participant, lang, incorrect_symbol, correct_symbol, callback):
        super(QtScanEnvelopeError, self).__init__(parent)
        self.setGeometry(QtCore.QRect(520, 140, 1400, 920))
        self.setObjectName("frame")
        self.config = config
        self.participant = participant
        self.lang = lang
        self.incorrect_symbol = incorrect_symbol
        self.correct_symbol = correct_symbol

        self.Heading = QtWidgets.QLabel(self)
        self.Heading.setGeometry(QtCore.QRect(20, 20, 1360, 200))
        self.Heading.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.Heading.setAlignment(QtCore.Qt.AlignCenter)
        self.Heading.setObjectName("Heading")

        self.Body = QtWidgets.QLabel(self)
        self.Body.setGeometry(QtCore.QRect(20, 120, 1360, 600))
        font_size = "48pt"
        if hasattr(self.lang, "Body_Font_Size"):
            font_size = self.lang.Body_Font_Size
        body_css = "font: " + font_size + " \"" + self.config.font + "\";"
        if hasattr(self.lang, "Body_CSS"):
            body_css += self.lang.Body_CSS
        self.Body.setStyleSheet(body_css)
        self.Body.setWordWrap(True)
        self.Body.setObjectName("Body")

        self.Button = QtWidgets.QPushButton(self)
        self.Button.setGeometry(QtCore.QRect(20, 720, 1360, 200))
        self.Button.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.Button.setDefault(False)
        self.Button.setObjectName("Button")
        self.Button.setEnabled(False)
        QtCore.QTimer.singleShot(self.config.button_timeout, lambda: self.Button.setEnabled(True))

        self.Button.clicked.connect(callback)

        self.re_translate_ui()

    def re_translate_ui(self):
        self.Heading.setText(Lang.filter(self.lang.Heading, self.participant))
        incorrect_symbol_text = "<span style=\"font-weight:550\">" + self.incorrect_symbol + "</span> (" + Symbol.get_unicode_symbol(
            self.incorrect_symbol) + ")"
        correct_symbol_text = "<span style=\"font-weight:550\">" + self.correct_symbol + "</span> (" + Symbol.get_unicode_symbol(
            self.correct_symbol) + ")"
        self.Body.setText(Lang.filter(self.lang.Body, self.participant)
                          .replace('?', incorrect_symbol_text, 1)
                          .replace('?', correct_symbol_text, 1))
        self.Button.setText(Lang.filter(self.lang.B_Ok, self.participant))
