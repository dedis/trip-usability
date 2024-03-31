from importlib import resources

from PyQt5 import QtWidgets, QtCore, QtGui

from app.utils.lang import Lang


class QtScanQRCode(QtWidgets.QFrame):
    def __init__(self, parent, config, participant, lang):
        super(QtScanQRCode, self).__init__(parent)
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

        self.SubHeading = QtWidgets.QLabel(self)
        self.SubHeading.setGeometry(QtCore.QRect(20, 220, 1360, 60))
        self.SubHeading.setStyleSheet("font: 48pt \"" + self.config.font + "\";")
        self.SubHeading.setAlignment(QtCore.Qt.AlignCenter)
        self.SubHeading.setObjectName("Heading")

        self.QR_Image = QtWidgets.QLabel(self)
        self.QR_Image.setGeometry(QtCore.QRect(500, 360, 400, 400))
        with resources.path("app.resources.images", "check-in-ticket.png") as image_path:
            self.QR_Image.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.QR_Image.setScaledContents(True)
        self.QR_Image.setObjectName("QR Code")

        # self.Camera_Image = QtWidgets.QLabel(self)
        # # self.thread = CameraThread(self)
        # # self.thread.changePixmap(self.setImage)
        # # self.worker =
        # #
        # # self.Camera_Image.move
        # # self.Camera_Image.setGeometry(QtCore.QRect(950, 360, 400, 400))
        #
        # # th.changePixmap.connect(self.setImage)
        # # th.start()
        #
        # # self.Caption = QtWidgets.QLabel(self)
        # # self.Caption.setGeometry(QtCore.QRect(400, 630, 600, 60))
        # # self.Caption.setStyleSheet("font: 48pt \"" + self.config.font + "\";")
        # # self.Caption.setAlignment(QtCore.Qt.AlignCenter)
        # # self.Caption.setObjectName("Heading")

        self.re_translate_ui()

    # @QtCore.pyqtSlot(QtGui.QImage)
    # def setImage(self, image):
    #     self.Camera_Image.setPixmap(QtGui.QPixmap.fromImage(image))

    def re_translate_ui(self):
        self.Heading.setText(Lang.filter(self.lang.Heading, self.participant))
        self.SubHeading.setText(Lang.filter(self.lang.SubHeading, self.participant))
