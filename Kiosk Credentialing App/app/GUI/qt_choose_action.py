from PyQt5 import QtWidgets, QtCore

from app.GUI.qt_button import QtButton
from app.utils.lang import Lang


class QtChooseAction(QtWidgets.QFrame):
    def __init__(self, parent, config, participant, lang, callback_left, callback_right):
        super(QtChooseAction, self).__init__(parent)
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

        self.ButtonLeft = QtButton(self, self.config, self.lang, QtCore.QRect(20, 720, 660, 200), callback_left)
        self.ButtonRight = QtButton(self, self.config, self.lang, QtCore.QRect(720, 720, 660, 200), callback_right)

        self.re_translate_ui()

    def re_translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.Heading.setText(Lang.filter(self.lang.Heading, self.participant))
        self.Body.setText(Lang.filter(self.lang.Body, self.participant))
        self.ButtonLeft.setText(Lang.filter(self.lang.B_Left, self.participant))
        self.ButtonRight.setText(Lang.filter(self.lang.B_Right, self.participant))
