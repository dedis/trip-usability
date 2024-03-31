from importlib import resources

from PyQt5 import QtWidgets, QtCore, QtGui

from app.utils.lang import Lang


class QtRealCredentialCreateInfo(QtWidgets.QWidget):
    def __init__(self, parent, config, participant, lang, symbol, callback_left, callback_right):
        super(QtRealCredentialCreateInfo, self).__init__(parent)
        self.config = config
        self.participant = participant
        self.lang = lang
        self.symbol = symbol

        self.Title = QtWidgets.QLabel(self)
        self.Title.setGeometry(QtCore.QRect(20, 10, 1880, 200))
        self.Title.setStyleSheet("font: 72pt \"" + self.config.font + "\";")
        self.Title.setTextFormat(QtCore.Qt.PlainText)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setScaledContents(False)
        self.Title.setObjectName("Title")

        # # Navigation Frame
        # self.Navigation = QtNavigation(self)
        # self.Navigation.setCurrentPage(QtNavigation.CREDENTIAL)

        # self.Heading = QtWidgets.QLabel(self)
        # self.Heading.setGeometry(QtCore.QRect(0, 200, 1920, 100))  # 1360, 100
        # self.Heading.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        # self.Heading.setAlignment(QtCore.Qt.AlignCenter)

        # Width: 1920-(300+250 +100+ 300+200 +100+ 300+230) = 140
        # Height: 1080-(150 - 220)=710

        height = 130 + 10 + 10  # (Spacing)

        self.Step1_Image = QtWidgets.QLabel(self)
        self.Step1_Image.setGeometry(QtCore.QRect(75, height + 150, 250, 250))
        with resources.path("app.resources.images", "check-in-ticket.png") as image_path:
            self.Step1_Image.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.Step1_Image.setScaledContents(True)

        self.Step1_Caption = QtWidgets.QLabel(self)
        self.Step1_Caption.setGeometry(QtCore.QRect(50, height + 100 + 320, 300, 300))
        self.Step1_Caption.setStyleSheet("font: 38pt \"" + self.config.font + "\";")
        self.Step1_Caption.setAlignment(QtCore.Qt.AlignHCenter)
        self.Step1_Caption.setWordWrap(True)

        width = 300 + 100  # (Spacing)

        self.Step2_Image = QtWidgets.QLabel(self)
        self.Step2_Image.setGeometry(QtCore.QRect(width, height + 70, 300, 336))
        with resources.path("app.resources.images", "printer_commit_" + symbol + ".png") as image_path:
            self.Step2_Image.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.Step2_Image.setScaledContents(True)

        self.Step2_Caption = QtWidgets.QLabel(self)
        self.Step2_Caption.setGeometry(QtCore.QRect(width, height + 100 + 320, 320, 300))
        self.Step2_Caption.setStyleSheet("font: 38pt \"" + self.config.font + "\";")
        self.Step2_Caption.setAlignment(QtCore.Qt.AlignHCenter)
        self.Step2_Caption.setWordWrap(True)

        width = width + 300 + 100  # (Spacing)

        self.Step3_Caption = QtWidgets.QLabel(self)
        self.Step3_Caption.setGeometry(QtCore.QRect(width, height + 140, 300, 550))
        self.Step3_Caption.setStyleSheet("font: 38pt \"" + self.config.font + "\";")
        # self.Step3_Caption.setAlignment(QtCore.Qt.AlignCenter)
        self.Step3_Caption.setWordWrap(True)

        self.Step3_Image = QtWidgets.QLabel(self)
        self.Step3_Image.setGeometry(QtCore.QRect(width + 300, height + 140, 176, 500))
        with resources.path("app.resources.images", "envelope_" + symbol + ".png") as image_path:
            self.Step3_Image.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.Step3_Image.setScaledContents(True)

        width = width + 300 + 180 + 50

        self.Step4_Caption = QtWidgets.QLabel(self)
        self.Step4_Caption.setGeometry(QtCore.QRect(width, height + 120, 300, 500))
        self.Step4_Caption.setStyleSheet("font: 38pt \"" + self.config.font + "\";")
        self.Step4_Caption.setAlignment(QtCore.Qt.AlignVCenter)
        self.Step4_Caption.setWordWrap(True)

        self.Step4_Image = QtWidgets.QLabel(self)
        self.Step4_Image.setGeometry(QtCore.QRect(width + 300, height + 60, 300, 600))
        with resources.path("app.resources.images", "printer_receipt_" + symbol + ".png") as image_path:
            self.Step4_Image.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.Step4_Image.setScaledContents(True)

        # self.TearWarning = QtWidgets.QLabel(self)
        # self.TearWarning.setGeometry(QtCore.QRect(170, 700, 400, 150))
        # self.TearWarning.setStyleSheet("font: 38pt \"" + self.config.font + "\";")
        # self.TearWarning.setWordWrap(True)

        self.ButtonLeft = QtWidgets.QPushButton(self)
        self.ButtonLeft.setGeometry(QtCore.QRect(20, 880, 920, 180))
        self.ButtonLeft.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.ButtonLeft.setDefault(False)
        self.ButtonLeft.setObjectName("ButtonLeft")

        self.ButtonRight = QtWidgets.QPushButton(self)
        self.ButtonRight.setGeometry(QtCore.QRect(980, 880, 920, 180))
        self.ButtonRight.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.ButtonRight.setDefault(False)
        self.ButtonRight.setObjectName("ButtonRight")

        self.ButtonLeft.setEnabled(False)
        QtCore.QTimer.singleShot(self.config.button_timeout, lambda: self.ButtonLeft.setEnabled(True))
        self.ButtonRight.setEnabled(False)
        QtCore.QTimer.singleShot(self.config.button_timeout, lambda: self.ButtonRight.setEnabled(True))

        self.ButtonLeft.clicked.connect(callback_left)
        self.ButtonRight.clicked.connect(callback_right)

        self.re_translate_ui()

    def re_translate_ui(self):
        self.Title.setText(Lang.filter(self.lang.Title, self.participant))
        # self.Heading.setText(Lang.filter(self.lang.Heading, self.participant))
        self.Step1_Caption.setText(Lang.filter(self.lang.Step1, self.participant))
        # self.TearWarning.setText(Lang.filter(self.lang.TearWarning, self.participant))
        self.Step2_Caption.setText(Lang.filter(self.lang.Step2, self.participant))
        self.Step3_Caption.setText(Lang.filter(self.lang.Step3, self.participant))
        self.Step4_Caption.setText(Lang.filter(self.lang.Step4, self.participant))
        self.ButtonLeft.setText(Lang.filter(self.lang.B_Left, self.participant))
        self.ButtonRight.setText(Lang.filter(self.lang.B_Right, self.participant))
