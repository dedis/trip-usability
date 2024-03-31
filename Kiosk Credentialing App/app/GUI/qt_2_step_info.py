from importlib import resources

from PyQt5 import QtWidgets, QtCore, QtGui

from app.utils.lang import Lang


class Qt2StepInfo(QtWidgets.QFrame):
    def __init__(self, parent, config, participant, lang, printed_symbol, callback):
        super(Qt2StepInfo, self).__init__(parent)
        self.setGeometry(QtCore.QRect(520, 140, 1400, 920))
        self.setObjectName("frame")
        self.config = config
        self.participant = participant
        self.lang = lang

        self.Heading = QtWidgets.QLabel(self)
        self.Heading.setGeometry(QtCore.QRect(20, 20, 1100, 200))
        self.Heading.setStyleSheet("font: 56pt \"" + self.config.font + "\";")
        self.Heading.setAlignment(QtCore.Qt.AlignCenter)
        self.Heading.setWordWrap(True)

        # Width: 1400-(200+20+200 +200+ 200+20+200) = 360
        self.Step1_Caption = QtWidgets.QLabel(self)
        self.Step1_Caption.setGeometry(QtCore.QRect(130, 280, 280, 350))
        self.Step1_Caption.setStyleSheet("font: 42pt \"" + self.config.font + "\";")
        self.Step1_Caption.setAlignment(QtCore.Qt.AlignVCenter)
        self.Step1_Caption.setWordWrap(True)

        self.Step1_Image = QtWidgets.QLabel(self)
        self.Step1_Image.setGeometry(QtCore.QRect(400, 200, 250, 500))
        with resources.path("app.resources.images", "printer_receipt_" + printed_symbol + ".png") as image_path:
            self.Step1_Image.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.Step1_Image.setScaledContents(True)

        self.Step2_Caption = QtWidgets.QLabel(self)
        self.Step2_Caption.setGeometry(QtCore.QRect(800, 280, 240, 350))
        self.Step2_Caption.setStyleSheet("font: 42pt \"" + self.config.font + "\";")
        self.Step2_Caption.setAlignment(QtCore.Qt.AlignVCenter)
        self.Step2_Caption.setWordWrap(True)

        self.Step2_Video = QtWidgets.QLabel(self)
        self.Step2_Video.setGeometry(QtCore.QRect(1125, 0, 150, 900))
        with resources.path("app.resources.images", "envelope_receipt_insert_" + printed_symbol + ".gif") as image_path:
            self.movie = QtGui.QMovie(str(image_path.absolute()))
            self.Step2_Video.setMovie(self.movie)
            self.movie.start()
        self.Step2_Video.setScaledContents(True)

        self.Button = QtWidgets.QPushButton(self)
        self.Button.setGeometry(QtCore.QRect(20, 720, 1000, 200))
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
