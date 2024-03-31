from PyQt5 import QtWidgets, QtCore, QtGui

from app.components.quiz import Quiz
from app.utils.lang import Lang


class QtQuizMultiple(QtWidgets.QFrame):
    def __init__(self, parent, config, participant, quiz, lang, callback):
        super(QtQuizMultiple, self).__init__(parent)
        self.setGeometry(QtCore.QRect(500, 140, 1400, 920))
        self.setObjectName("frame")
        self.config = config
        self.participant = participant
        self.quiz = quiz
        self.lang = lang
        self.callback = callback

        self.Heading = QtWidgets.QLabel(self)
        self.Heading.setGeometry(QtCore.QRect(20, 20, 1360, 100))
        self.Heading.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.Heading.setAlignment(QtCore.Qt.AlignCenter)
        self.Heading.setObjectName("Heading")

        self.Body = QtWidgets.QLabel(self)
        body_height = 300 if not hasattr(self.lang, "Body_Height") else self.lang.Body_Height
        self.Body.setGeometry(QtCore.QRect(20, 100, 1360, body_height))
        font_size = "48pt" if not hasattr(self.lang, "Body_Font_Size") else self.lang.Body_Font_Size
        body_css = "font: " + font_size + " \"" + self.config.font + "\";"
        if hasattr(self.lang, "Body_CSS"):
            body_css += self.lang.Body_CSS
        self.Body.setStyleSheet(body_css)
        self.Body.setAlignment(QtCore.Qt.AlignCenter)
        self.Body.setWordWrap(True)
        self.Body.setObjectName("Body")

        # layout = QtWidgets.QHBoxLayout()
        height = 0
        start_height = body_height + 100

        font_size = 42 if not hasattr(self.lang, "Label_Font_Size") else self.lang.Label_Font_Size
        font = QtGui.QFont(self.config.font, font_size)

        self.gui_options = []
        for option in self.quiz.options:
            o = QtWidgets.QCheckBox(self)
            o.setGeometry(QtCore.QRect(20, start_height + height, 1360, 100))
            o.setText(option)
            o.setFont(font)
            o.toggled.connect(lambda: self.enable_submit_button())
            o.setStyleSheet(
                "QCheckBox::indicator { width:90px; height: 90px; background: none;}")
            self.gui_options.append(o)

            height += 100

        self.Button = QtWidgets.QPushButton(self)
        self.Button.setGeometry(QtCore.QRect(20, 720, 1320, 200))
        font_size = "64pt"
        if hasattr(self.lang, "B_Top_Font_Size"):
            font_size = self.lang.Body_Font_Size
        body_css = "font: " + font_size + " \"" + self.config.font + "\";"
        self.Button.setStyleSheet(body_css)
        self.Button.setDefault(False)
        self.Button.setObjectName("ButtonLeft")

        self.Button.setEnabled(False)
        self.Button.clicked.connect(self.evaluate_selection)

        self.re_translate_ui()

    def enable_submit_button(self):
        selected_options = set()
        for option in self.gui_options:
            if option.isChecked():
                selected_options.add(option.text())

        if len(selected_options) > 0:
            self.Button.setEnabled(True)
        else:
            self.Button.setEnabled(False)

    def evaluate_selection(self):
        selected_options = set()
        for option in self.gui_options:
            if option.isChecked():
                selected_options.add(option.text())

        if len(self.quiz.correct_options) == len(selected_options) and \
                len(set(selected_options).intersection(self.quiz.correct_options)) == len(self.quiz.correct_options):
            self.callback(Quiz.CORRECT, selected_options)
        else:
            self.callback(Quiz.INCORRECT, selected_options)

    def re_translate_ui(self):
        self.Heading.setText(Lang.filter(self.lang.Heading, self.participant))
        self.Body.setText(Lang.filter(self.lang.Body, self.participant))
        self.Button.setText(Lang.filter(self.lang.B_Submit, self.participant))
        # self.b1.setText("Text")
        # self.b2.setText("Text2")
