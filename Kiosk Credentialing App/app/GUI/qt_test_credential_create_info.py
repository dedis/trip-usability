from importlib import resources

from PyQt5 import QtWidgets, QtCore, QtGui

from app.utils.lang import Lang


class QtTestCredentialCreateInfo(QtWidgets.QFrame):
    def __init__(self, parent, config, participant, lang, symbol, callback):
        super(QtTestCredentialCreateInfo, self).__init__(parent)
        self.setGeometry(QtCore.QRect(520, 140, 1400, 920))
        self.setObjectName("frame")
        self.config = config
        self.participant = participant
        self.lang = lang

        self.Heading = QtWidgets.QLabel(self)
        self.Heading.setGeometry(QtCore.QRect(20, 20, 1360, 200))  # 1360, 100
        self.Heading.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.Heading.setAlignment(QtCore.Qt.AlignCenter)

        # Width: 1400-(300+20+200 +100+ 300+20+200) = 360
        left_margin = int((1400 - (300 + 20 + 200 + 100 + 300 + 20 + 200)) / 2)
        self.Step1_Caption = QtWidgets.QLabel(self)
        self.Step1_Caption.setGeometry(QtCore.QRect(left_margin, 210, 300, 400))
        self.Step1_Caption.setStyleSheet("font: 42pt \"" + self.config.font + "\";")
        self.Step1_Caption.setAlignment(QtCore.Qt.AlignVCenter)
        self.Step1_Caption.setWordWrap(True)

        self.Step1_Image = QtWidgets.QLabel(self)
        self.Step1_Image.setGeometry(QtCore.QRect(left_margin + 320, 200, 178, 504))
        with resources.path("app.resources.images", "envelope_" + symbol + ".png") as image_path:
            self.Step1_Image.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.Step1_Image.setScaledContents(True)

        self.Step2_Caption = QtWidgets.QLabel(self)
        self.Step2_Caption.setGeometry(QtCore.QRect(left_margin + 620, 210, 300, 400))
        self.Step2_Caption.setStyleSheet("font: 42pt \"" + self.config.font + "\";")
        self.Step2_Caption.setAlignment(QtCore.Qt.AlignVCenter)
        self.Step2_Caption.setWordWrap(True)

        self.Step2_Image = QtWidgets.QLabel(self)
        self.Step2_Image.setGeometry(QtCore.QRect(left_margin + 940, 200, 250, 500))
        with resources.path("app.resources.images", "printer_receipt_" + symbol + ".png") as image_path:
            self.Step2_Image.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.Step2_Image.setScaledContents(True)

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
        self.Step1_Caption.setText(Lang.filter(self.lang.Step1, self.participant))
        self.Step2_Caption.setText(Lang.filter(self.lang.Step2, self.participant))
        self.Button.setText(Lang.filter(self.lang.B_Ok, self.participant))
