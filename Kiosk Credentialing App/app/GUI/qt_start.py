from PyQt5 import QtWidgets, QtCore

from app.GUI.qt_button import QtButton
from app.utils.lang import Lang


class QtStart(QtWidgets.QFrame):
    def __init__(self, parent, config, participant, lang, callback):
        super(QtStart, self).__init__(parent)
        self.setGeometry(QtCore.QRect(520, 140, 1400, 920))
        self.setObjectName("frame")
        self.config = config
        self.participant = participant
        self.lang = lang
        self.callback = callback

        self.Heading = QtWidgets.QLabel(self)
        self.Heading.setGeometry(QtCore.QRect(20, 20, 1360, 100))
        self.Heading.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.Heading.setAlignment(QtCore.Qt.AlignCenter)
        self.Heading.setObjectName("Heading")

        self.SubHeading = QtWidgets.QLabel(self)
        self.SubHeading.setGeometry(QtCore.QRect(20, 320, 1360, 200))
        font_size = "48pt"
        if hasattr(self.lang, "SubHeading_Font_Size"):
            font_size = self.lang.SubHeading_Font_Size
        body_css = "font: " + font_size + " \"" + self.config.font + "\";"
        if hasattr(self.lang, "SubHeading_CSS"):
            body_css += self.lang.SubHeading_CSS
        self.SubHeading.setStyleSheet(body_css)
        self.SubHeading.setAlignment(QtCore.Qt.AlignCenter)

        self.Button = QtButton(self, config, lang, QtCore.QRect(20, 720, 1360, 200), callback)

        self.re_translate_ui()

    def re_translate_ui(self):
        self.Heading.setText(Lang.filter(self.lang.Heading, self.participant))
        self.SubHeading.setText(Lang.filter(self.lang.SubHeading, self.participant))
        self.Button.setText(Lang.filter(self.lang.B_Ok, self.participant))
