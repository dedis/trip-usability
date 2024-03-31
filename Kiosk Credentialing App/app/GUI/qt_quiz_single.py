from PyQt5 import QtWidgets, QtCore

from app.utils.lang import Lang


class QtQuizSingle(QtWidgets.QFrame):
    def __init__(self, parent, config, participant, lang, callback_top, callback_bottom):
        super(QtQuizSingle, self).__init__(parent)
        self.setGeometry(QtCore.QRect(500, 140, 1400, 920))
        self.setObjectName("frame")
        self.config = config
        self.participant = participant
        self.lang = lang

        self.Heading = QtWidgets.QLabel(self)
        self.Heading.setGeometry(QtCore.QRect(20, 20, 1360, 100))
        self.Heading.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.Heading.setAlignment(QtCore.Qt.AlignCenter)
        self.Heading.setObjectName("Heading")

        self.Body = QtWidgets.QLabel(self)
        self.Body.setGeometry(QtCore.QRect(20, 100, 1360, 400))
        font_size = "48pt"
        if hasattr(self.lang, "Body_Font_Size"):
            font_size = self.lang.Body_Font_Size
        body_css = "font: " + font_size + " \"" + self.config.font + "\";"
        if hasattr(self.lang, "Body_CSS"):
            body_css += self.lang.Body_CSS
        self.Body.setStyleSheet(body_css)
        self.Body.setAlignment(QtCore.Qt.AlignCenter)
        self.Body.setWordWrap(True)
        self.Body.setObjectName("Body")

        self.ButtonTop = QtWidgets.QPushButton(self)
        self.ButtonTop.setGeometry(QtCore.QRect(20, 500, 1320, 200))
        font_size = "48pt"
        if hasattr(self.lang, "B_Top_Font_Size"):
            font_size = self.lang.Body_Font_Size
        body_css = "font: " + font_size + " \"" + self.config.font + "\";"
        self.ButtonTop.setStyleSheet(body_css)
        self.ButtonTop.setDefault(False)
        self.ButtonTop.setObjectName("ButtonLeft")

        self.ButtonBottom = QtWidgets.QPushButton(self)
        self.ButtonBottom.setGeometry(QtCore.QRect(20, 720, 1320, 200))
        font_size = "48pt"
        if hasattr(self.lang, "B_Bot_Font_Size"):
            font_size = self.lang.Body_Font_Size
        body_css = "font: " + font_size + " \"" + self.config.font + "\";"
        self.ButtonBottom.setStyleSheet(body_css)
        self.ButtonBottom.setDefault(False)
        self.ButtonBottom.setObjectName("ButtonRight")

        self.ButtonTop.setEnabled(False)
        QtCore.QTimer.singleShot(self.config.button_timeout, lambda: self.ButtonTop.setEnabled(True))
        self.ButtonBottom.setEnabled(False)
        QtCore.QTimer.singleShot(self.config.button_timeout, lambda: self.ButtonBottom.setEnabled(True))

        self.ButtonTop.clicked.connect(callback_top)
        self.ButtonBottom.clicked.connect(callback_bottom)

        self.re_translate_ui()

    def re_translate_ui(self):
        self.Heading.setText(Lang.filter(self.lang.Heading, self.participant))
        self.Body.setText(Lang.filter(self.lang.Body, self.participant))
        self.ButtonTop.setText(Lang.filter(self.lang.B_Top, self.participant))
        self.ButtonBottom.setText(Lang.filter(self.lang.B_Bot, self.participant))
