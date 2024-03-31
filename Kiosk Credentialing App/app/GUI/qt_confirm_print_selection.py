from importlib import resources

from PyQt5 import QtWidgets, QtCore, QtGui

from app.components.symbol import Symbol
from app.utils.lang import Lang


class QtConfirmPrintSelection(QtWidgets.QFrame):
    def __init__(self, parent, config, participant, lang,
                 correct_symbol, correct_callback, incorrect_callback):
        super(QtConfirmPrintSelection, self).__init__(parent)
        self.setGeometry(QtCore.QRect(520, 140, 1400, 920))
        self.setObjectName("frame")
        self.config = config
        self.participant = participant
        self.lang = lang

        self.Heading = QtWidgets.QLabel(self)
        self.Heading.setGeometry(QtCore.QRect(20, 20, 1360, 200))
        self.Heading.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.Heading.setAlignment(QtCore.Qt.AlignCenter)
        self.Heading.setObjectName("Heading")

        self.Body = QtWidgets.QLabel(self)
        self.Body.setGeometry(QtCore.QRect(20, 210, 1000, 400))
        font_size = "48pt"
        if hasattr(self.lang, "Body_Font_Size"):
            font_size = self.lang.Body_Font_Size
        body_css = "font: " + font_size + " \"" + self.config.font + "\";"
        if hasattr(self.lang, "Body_CSS"):
            body_css += self.lang.Body_CSS
        self.Body.setStyleSheet(body_css)
        self.Body.setWordWrap(True)

        if hasattr(self.lang, "TearWarning"):
            self.TearWarning = QtWidgets.QLabel(self)
            self.TearWarning.setGeometry(QtCore.QRect(450, 420, 500, 300))
            font_size = "48pt"
            if hasattr(self.lang, "Body_Font_Size"):
                font_size = self.lang.Body_Font_Size
            body_css = "font: " + font_size + " \"" + self.config.font + "\";"
            if hasattr(self.lang, "Body_CSS"):
                body_css += self.lang.Body_CSS
            self.TearWarning.setStyleSheet(body_css)
            self.TearWarning.setWordWrap(True)
            self.TearWarning.setObjectName("Body")

        self.Printer_Image = QtWidgets.QLabel(self)
        self.Printer_Image.setGeometry(QtCore.QRect(1020, 210, 300, 350))
        with resources.path("app.resources.images", "printer.png") as image_path:
            self.Printer_Image.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.Printer_Image.setScaledContents(True)

        self.SquareButton = QtWidgets.QPushButton(self)
        self.SquareButton.setGeometry(QtCore.QRect(20, 720, 440, 200))
        self.SquareButton.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.SquareButton.setDefault(False)
        self.SquareButton.setEnabled(False)
        QtCore.QTimer.singleShot(self.config.button_timeout, lambda: self.SquareButton.setEnabled(True))

        self.CircleButton = QtWidgets.QPushButton(self)
        self.CircleButton.setGeometry(QtCore.QRect(460, 720, 440, 200))
        self.CircleButton.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.CircleButton.setDefault(False)
        self.CircleButton.setEnabled(False)
        QtCore.QTimer.singleShot(self.config.button_timeout, lambda: self.CircleButton.setEnabled(True))

        self.TriangleButton = QtWidgets.QPushButton(self)
        self.TriangleButton.setGeometry(QtCore.QRect(920, 720, 440, 200))
        self.TriangleButton.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.TriangleButton.setDefault(False)
        self.TriangleButton.setEnabled(False)
        QtCore.QTimer.singleShot(self.config.button_timeout, lambda: self.TriangleButton.setEnabled(True))

        callback_square = incorrect_callback
        callback_circle = incorrect_callback
        callback_triangle = incorrect_callback
        if correct_symbol == Symbol.SQUARE:
            callback_square = correct_callback
        elif correct_symbol == Symbol.CIRCLE:
            callback_circle = correct_callback
        elif correct_symbol == Symbol.TRIANGLE:
            callback_triangle = correct_callback

        self.SquareButton.clicked.connect(callback_square)
        self.CircleButton.clicked.connect(callback_circle)
        self.TriangleButton.clicked.connect(callback_triangle)

        self.re_translate_ui()

    def re_translate_ui(self):
        self.Heading.setText(Lang.filter(self.lang.Heading, self.participant))
        self.Body.setText(Lang.filter(self.lang.Body, self.participant))
        self.TearWarning.setText(Lang.filter(self.lang.TearWarning, self.participant))
