from PyQt5 import QtWidgets, QtCore, QtGui


class QtNavigation(QtWidgets.QFrame):
    CHECKIN = "Check-In"
    CREDENTIAL = "Credential"
    TEST_CREDENTIAL = "TestCredential"
    NONE = "None"

    def __init__(self, parent, test_cred=True):
        super(QtNavigation, self).__init__(parent)
        self.setGeometry(QtCore.QRect(720, 0, 1200, 131))
        self.test_cred = test_cred

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(36)
        self.setFont(font)
        self.setObjectName("Navigation")

        width_size = 1200
        if test_cred:
            width_size = int(width_size / 3)
        else:
            width_size = int(width_size / 2)

        border_width = 5
        height = 0

        self.CheckIn = QtWidgets.QLabel(self)
        self.CheckIn.setGeometry(QtCore.QRect(width_size * 0 + border_width * 2, height, width_size, 80))
        self.CheckIn.setObjectName("CheckIn")
        self.CheckIn.setFont(font)
        self.CheckIn.setAlignment(QtCore.Qt.AlignCenter)
        self.CheckIn.setStyleSheet("border: " + str(border_width) + "px solid black;")
        self.CheckIn.setText("Check-In")

        self.Credential = QtWidgets.QLabel(self)
        self.Credential.setGeometry(QtCore.QRect(width_size * 1 + border_width, height, width_size, 80))
        self.Credential.setObjectName("Credential")
        self.Credential.setFont(font)
        self.Credential.setAlignment(QtCore.Qt.AlignCenter)
        self.Credential.setStyleSheet("border: " + str(border_width) + "px solid black;")
        self.Credential.setText("Credential")

        if test_cred:
            self.TestCredential = QtWidgets.QLabel(self)
            self.TestCredential.setGeometry(QtCore.QRect(width_size * 2, height, width_size, 80))
            self.TestCredential.setObjectName("TestCredential")
            self.TestCredential.setFont(font)
            self.TestCredential.setAlignment(QtCore.Qt.AlignCenter)
            self.TestCredential.setStyleSheet("border: " + str(border_width) + "px solid black;")
            self.TestCredential.setText("Extra")

    def setCurrentPage(self, page):
        neutral_font = QtGui.QFont()
        neutral_font.setFamily("Helvetica")
        neutral_font.setPointSize(42)

        bold_font = QtGui.QFont()
        bold_font.setFamily("Helvetica")
        bold_font.setPointSize(42)
        bold_font.setBold(True)
        bold_font.setWeight(70)

        self.CheckIn.setFont(neutral_font)
        self.Credential.setFont(neutral_font)
        if self.test_cred:
            self.TestCredential.setFont(neutral_font)

        if page == QtNavigation.CHECKIN:
            self.CheckIn.setFont(bold_font)
        elif page == QtNavigation.CREDENTIAL:
            self.Credential.setFont(bold_font)
        elif page == QtNavigation.TEST_CREDENTIAL and self.test_cred:
            self.TestCredential.setFont(bold_font)
