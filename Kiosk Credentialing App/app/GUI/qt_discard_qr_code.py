from importlib import resources

from PyQt5 import QtWidgets, QtCore, QtGui

from app.utils.lang import Lang


class Qt_Discard_QR_Code(QtWidgets.QFrame):
    def __init__(self, parent, config, participant, lang, callback_left, callback_right):
        super(Qt_Discard_QR_Code, self).__init__(parent)
        self.setGeometry(QtCore.QRect(520, 140, 1400, 920))
        self.setObjectName("frame")
        self.config = config
        self.participant = participant
        self.lang = lang

        self.Heading = QtWidgets.QLabel(self)
        self.Heading.setGeometry(QtCore.QRect(20, 20, 1360, 100))  # 1360, 100
        self.Heading.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.Heading.setAlignment(QtCore.Qt.AlignCenter)
        self.Heading.setObjectName("Heading")

        self.SubHeading = QtWidgets.QLabel(self)
        self.SubHeading.setGeometry(QtCore.QRect(20, 120, 1360, 60))  # 1360, 180
        self.SubHeading.setStyleSheet("font: 48pt \"" + self.config.font + "\";")
        self.SubHeading.setAlignment(QtCore.Qt.AlignCenter)
        self.SubHeading.setObjectName("Heading")

        # Width: 1360-(400+20+200+20+400) = 320 | /2 = 160
        # QR + Space + RightArrow + Space + TrashCan

        self.QRCode = QtWidgets.QLabel(self)
        self.QRCode.setGeometry(QtCore.QRect(160, 230, 400, 400))
        with resources.path("app.resources.images", "check-in-ticket.png") as image_path:
            self.QRCode.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.QRCode.setScaledContents(True)
        self.QRCode.setObjectName("QR Code")

        self.RightArrow = QtWidgets.QLabel(self)
        self.RightArrow.setGeometry(QtCore.QRect(580, 350, 300, 120))
        with resources.path("app.resources.images", "right_arrow.png") as image_path:
            self.RightArrow.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.RightArrow.setScaledContents(True)
        self.RightArrow.setObjectName("QR Code")

        self.TrashCan = QtWidgets.QLabel(self)
        self.TrashCan.setGeometry(QtCore.QRect(900, 230, 400, 400))
        with resources.path("app.resources.images", "trash_can.png") as image_path:
            self.TrashCan.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.TrashCan.setScaledContents(True)
        self.TrashCan.setObjectName("QR Code")

        self.ButtonLeft = QtWidgets.QPushButton(self)
        self.ButtonLeft.setGeometry(QtCore.QRect(20, 720, 660, 200))
        self.ButtonLeft.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.ButtonLeft.setDefault(False)
        self.ButtonLeft.setObjectName("ButtonLeft")

        self.ButtonRight = QtWidgets.QPushButton(self)
        self.ButtonRight.setGeometry(QtCore.QRect(720, 720, 660, 200))
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
        self.Heading.setText(Lang.filter(self.lang.Heading, self.participant))
        self.SubHeading.setText(Lang.filter(self.lang.SubHeading, self.participant))
        self.ButtonLeft.setText(Lang.filter(self.lang.B_Left, self.participant))
        self.ButtonRight.setText(Lang.filter(self.lang.B_Right, self.participant))
