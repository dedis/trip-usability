from importlib import resources

from PyQt5 import QtWidgets, QtCore, QtGui

from app.components.symbol import Symbol
from app.utils.lang import Lang


class QtConfirmPrint(QtWidgets.QFrame):
    def __init__(self, parent, config, participant, lang, printed_symbol, callback):
        super(QtConfirmPrint, self).__init__(parent)
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
        self.Heading.setObjectName("Heading")

        self.Body = QtWidgets.QLabel(self)
        self.Body.setGeometry(QtCore.QRect(20, 210, 900, 300))
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
            self.TearWarning.setGeometry(QtCore.QRect(400, 400, 500, 300))
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
        self.Printer_Image.setGeometry(QtCore.QRect(980, 200, 350, 420))
        with resources.path("app.resources.images", "printer_commit_" + printed_symbol + ".png") as image_path:
            self.Printer_Image.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.Printer_Image.setScaledContents(True)

        self.Button = QtWidgets.QPushButton(self)
        self.Button.setGeometry(QtCore.QRect(20, 720, 1360, 200))
        self.Button.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.Button.setDefault(False)
        self.Button.setEnabled(False)
        QtCore.QTimer.singleShot(self.config.button_timeout, lambda: self.Button.setEnabled(True))

        self.Button.clicked.connect(callback)

        self.re_translate_ui()

    def re_translate_ui(self):
        self.Heading.setText(Lang.filter(self.lang.Heading, self.participant))
        symbol_text = "<span style=\"font-weight:550\">" + self.printed_symbol + "</span> (" + Symbol.get_unicode_symbol(
            self.printed_symbol) + ")"
        self.Body.setText(Lang.filter(self.lang.Body, self.participant).replace('?', symbol_text))
        self.TearWarning.setText(Lang.filter(self.lang.TearWarning, self.participant))
        self.Button.setText(Lang.filter(self.lang.B_Ok, self.participant))
