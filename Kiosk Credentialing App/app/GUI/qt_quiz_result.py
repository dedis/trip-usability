from importlib import resources

from PyQt5 import QtWidgets, QtCore, QtGui

from app.components.quiz import Quiz
from app.utils.lang import Lang


class QtQuizResult(QtWidgets.QFrame):

    def __init__(self, parent, config, participant, lang, result, callback):
        super(QtQuizResult, self).__init__(parent)
        self.setGeometry(QtCore.QRect(500, 140, 1400, 920))
        self.setObjectName("frame")
        self.config = config
        self.participant = participant
        self.lang = lang

        self.Heading = QtWidgets.QLabel(self)
        self.Heading.setGeometry(QtCore.QRect(20, 20, 1360, 100))
        self.Heading.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.Heading.setAlignment(QtCore.Qt.AlignCenter)

        self.SubHeading = QtWidgets.QLabel(self)
        self.SubHeading.setGeometry(QtCore.QRect(20, 100, 1360, 200))
        font_size = "48pt"
        if hasattr(self.lang, "SubHeading_Font_Size"):
            font_size = self.lang.SubHeading_Font_Size
        body_css = "font: " + font_size + " \"" + self.config.font + "\";"
        if hasattr(self.lang, "SubHeading_CSS"):
            body_css += self.lang.SubHeading_CSS
        self.SubHeading.setStyleSheet(body_css)
        self.SubHeading.setAlignment(QtCore.Qt.AlignCenter)
        self.SubHeading.setWordWrap(True)

        self.ResultImage = QtWidgets.QLabel(self)
        self.ResultImage.setGeometry(QtCore.QRect(560, 300, 100, 100))
        self.ResultImage.setScaledContents(True)

        self.ResultText = QtWidgets.QLabel(self)
        self.ResultText.setGeometry(QtCore.QRect(680, 300, 300, 100))
        self.ResultText.setAlignment(QtCore.Qt.AlignVCenter)
        self.ResultText.setStyleSheet("font: " + font_size + " \"" + self.config.font + "\";")

        if result == Quiz.CORRECT:
            with resources.path("app.resources.images", "correct.png") as image_path:
                self.ResultImage.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
            self.ResultText.setText("<span style=\"color:green;\">Correct</span>")
        else:
            with resources.path("app.resources.images", "incorrect.png") as image_path:
                self.ResultImage.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
            self.ResultText.setText("<span style=\"color:red;\">Incorrect</span>")

        self.Body = QtWidgets.QLabel(self)
        self.Body.setGeometry(QtCore.QRect(20, 420, 1380, 300))
        self.Body.setAlignment(QtCore.Qt.AlignCenter)
        font_size = "48pt" if not hasattr(self.lang, "Body_Font_Size") else self.lang.Body_Font_Size
        body_css = "font: " + font_size + " \"" + self.config.font + "\";"
        if hasattr(self.lang, "Body_CSS"):
            body_css += self.lang.Body_CSS
        self.Body.setStyleSheet(body_css)
        self.Body.setWordWrap(True)

        self.Button = QtWidgets.QPushButton(self)
        self.Button.setGeometry(QtCore.QRect(20, 720, 1360, 200))
        font_size = "64pt"
        if hasattr(self.lang, "B_Bot_Font_Size"):
            font_size = self.lang.Body_Font_Size
        body_css = "font: " + font_size + " \"" + self.config.font + "\";"
        self.Button.setStyleSheet(body_css)
        self.Button.setDefault(False)
        self.Button.setEnabled(False)
        QtCore.QTimer.singleShot(self.config.button_timeout, lambda: self.Button.setEnabled(True))

        self.Button.clicked.connect(callback)

        self.re_translate_ui()

    def re_translate_ui(self):
        self.Heading.setText(Lang.filter(self.lang.Heading, self.participant))
        self.SubHeading.setText(Lang.filter(self.lang.SubHeading, self.participant))
        self.Body.setText(Lang.filter(self.lang.Body, self.participant))
        self.Button.setText(Lang.filter(self.lang.B_Ok, self.participant))
