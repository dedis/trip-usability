from importlib import resources

from PyQt5 import QtWidgets, QtCore, QtGui

from app.utils.lang import Lang


class QtConfirmStatus(QtWidgets.QFrame):
    def __init__(self, parent, config, participant, lang, callback):
        super(QtConfirmStatus, self).__init__(parent)
        self.setGeometry(QtCore.QRect(520, 140, 1400, 920))
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
        self.Body.setGeometry(QtCore.QRect(20, 120, 1360, 300))
        font_size = "48pt"
        if hasattr(self.lang, "Body_Font_Size"):
            font_size = self.lang.Body_Font_Size
        body_css = "font: " + font_size + " \"" + self.config.font + "\";"
        if hasattr(self.lang, "Body_CSS"):
            body_css += self.lang.Body_CSS
        self.Body.setStyleSheet(body_css)
        self.Body.setWordWrap(True)
        self.Body.setObjectName("Body")

        self.CheckInImage = QtWidgets.QLabel(self)
        self.CheckInImage.setScaledContents(True)
        self.CheckedImage = QtWidgets.QLabel(self)
        self.CheckedImage.setScaledContents(True)
        self.RightArrow1Image = QtWidgets.QLabel(self)
        self.RightArrow1Image.setScaledContents(True)
        self.RealCredentialImage = QtWidgets.QLabel(self)
        self.RealCredentialImage.setScaledContents(True)

        self.RightArrow2Image = QtWidgets.QLabel(self)
        self.RightArrow2Image.setScaledContents(True)
        self.TestCredentialImage = QtWidgets.QLabel(self)
        self.TestCredentialImage.setScaledContents(True)

        self.CheckInCaption = QtWidgets.QLabel(self)
        self.CheckInCaption.setStyleSheet("font: 42pt \"" + self.config.font + "\";")
        self.CheckInCaption.setAlignment(QtCore.Qt.AlignCenter)
        self.RealCredentialCaption = QtWidgets.QLabel(self)
        self.RealCredentialCaption.setStyleSheet("font: 42pt \"" + self.config.font + "\";")
        self.RealCredentialCaption.setAlignment(QtCore.Qt.AlignCenter)
        self.TestCredentialCaption = QtWidgets.QLabel(self)
        self.TestCredentialCaption.setStyleSheet("font: 42pt \"" + self.config.font + "\";")
        self.TestCredentialCaption.setAlignment(QtCore.Qt.AlignCenter)

        # height = 920 - (120 + 300 + 200 + 200 + 100) =
        if participant.ab_test_credentials:
            # width = 1400 - (200 + 25 + 200 + 25 + 200 + 25 + 200 + 25 + 200) = 300 / 2 = 150
            left_margin = 150
        else:
            # width = 1400 - (200 + 25 + 200 + 25 + 200) = 750 / 2 = 375
            left_margin = 375

        self.CheckInImage.setGeometry(QtCore.QRect(left_margin, 420, 200, 200))
        with resources.path("app.resources.images", "check-in.png") as image_path:
            self.CheckInImage.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.CheckInCaption.setGeometry(QtCore.QRect(left_margin - 25, 620, 250, 100))

        self.CheckedImage.setGeometry(QtCore.QRect(left_margin + 135, 400, 100, 100))
        with resources.path("app.resources.images", "correct.png") as image_path:
            self.CheckedImage.setPixmap(QtGui.QPixmap(str(image_path.absolute())))

        self.RightArrow1Image.setGeometry(QtCore.QRect(left_margin + 225, 420, 200, 200))
        with resources.path("app.resources.images", "right_thin_arrow.png") as image_path:
            self.RightArrow1Image.setPixmap(QtGui.QPixmap(str(image_path.absolute())))

        self.RealCredentialImage.setGeometry(QtCore.QRect(left_margin + 450, 420, 200, 200))
        self.RealCredentialCaption.setGeometry(QtCore.QRect(left_margin + 350, 620, 400, 100))

        if participant.ab_test_credentials:
            self.with_test_credentials()
        else:
            self.without_test_credentials()

        self.Button = QtWidgets.QPushButton(self)
        self.Button.setGeometry(QtCore.QRect(20, 720, 1360, 200))
        self.Button.setStyleSheet("font: 64pt \"" + self.config.font + "\";")
        self.Button.setDefault(False)
        self.Button.setEnabled(False)
        QtCore.QTimer.singleShot(self.config.button_timeout, lambda: self.Button.setEnabled(True))

        self.Button.clicked.connect(callback)

        self.re_translate_ui()

    def without_test_credentials(self):
        with resources.path("app.resources.images", "credential.png") as image_path:
            self.RealCredentialImage.setPixmap(QtGui.QPixmap(str(image_path.absolute())))

        self.TestCredentialCaption.destroy()

    def with_test_credentials(self):
        with resources.path("app.resources.images", "real_credential.png") as image_path:
            self.RealCredentialImage.setPixmap(QtGui.QPixmap(str(image_path.absolute())))

        self.RightArrow2Image.setGeometry(QtCore.QRect(825, 420, 200, 200))
        with resources.path("app.resources.images", "right_thin_arrow.png") as image_path:
            self.RightArrow2Image.setPixmap(QtGui.QPixmap(str(image_path.absolute())))

        self.TestCredentialImage.setGeometry(QtCore.QRect(1050, 420, 200, 200))
        with resources.path("app.resources.images", "test_credential.png") as image_path:
            self.TestCredentialImage.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.TestCredentialCaption.setGeometry(QtCore.QRect(950, 620, 400, 100))

        self.TestCredentialCaption.setText(Lang.filter(self.lang.TestCredentialCaption, self.participant))

        # self.CheckInCaption.setGeometry(QtCore.QRect(270, 520, 200, 100))
        # self.CredentialCaption.setGeometry(QtCore.QRect(530, 520, 300, 100))
        # self.PlusCaption.setGeometry(QtCore.QRect(900, 520, 200, 100))

    def re_translate_ui(self):
        self.Heading.setText(Lang.filter(self.lang.Heading, self.participant))
        self.Body.setText(Lang.filter(self.lang.Body, self.participant))
        self.CheckInCaption.setText(Lang.filter(self.lang.CheckInCaption, self.participant))
        self.RealCredentialCaption.setText(Lang.filter(self.lang.RealCredentialCaption, self.participant))
        self.Button.setText(Lang.filter(self.lang.B_Ok, self.participant))
