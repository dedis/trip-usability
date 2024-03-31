from importlib import resources

from PyQt5 import QtWidgets, QtCore, QtGui

from app.GUI.qt_2_step_info import Qt2StepInfo
from app.GUI.qt_choose_action import QtChooseAction
from app.GUI.qt_confirm_action import QtConfirmAction
from app.GUI.qt_confirm_print import QtConfirmPrint
from app.GUI.qt_confirm_print_full import QtConfirmPrintFull
from app.GUI.qt_confirm_print_selection import QtConfirmPrintSelection
from app.GUI.qt_confirm_status import QtConfirmStatus
from app.GUI.qt_discard_qr_code import Qt_Discard_QR_Code
from app.GUI.qt_quiz_multiple import QtQuizMultiple
from app.GUI.qt_quiz_result import QtQuizResult
from app.GUI.qt_quiz_result_choose import QtQuizResultChoose
from app.GUI.qt_quiz_single import QtQuizSingle
from app.GUI.qt_scan_envelope import QtScanEnvelope
from app.GUI.qt_scan_envelope_error import QtScanEnvelopeError
from app.GUI.qt_scan_qr_code import QtScanQRCode
from app.GUI.qt_start import QtStart
from app.GUI.qt_start_facilitator import QtStartFacilitator
from app.GUI.qt_test_credential_create_info import QtTestCredentialCreateInfo


class MainFrame(QtWidgets.QWidget):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.setObjectName("Application")
        self.config = config

        self.Logo = QtWidgets.QLabel(self)
        self.Logo.setGeometry(QtCore.QRect(20, 140, 460, 800))
        with resources.path("app.resources.images", "fun_art.png") as image_path:
            self.Logo.setPixmap(QtGui.QPixmap(str(image_path.absolute())))
        self.Logo.setScaledContents(True)
        self.Logo.setObjectName("Logo")

        self.Title = QtWidgets.QLabel(self)
        self.Title.setGeometry(QtCore.QRect(20, 10, 900, 131))
        self.Title.setStyleSheet("font: 72pt \"" + self.config.font + "\";")
        self.Title.setTextFormat(QtCore.Qt.PlainText)
        self.Title.setScaledContents(False)
        self.Title.setObjectName("Title")

        self.re_translate_ui()

        # Navigation Frame
        # self.Navigation = QtNavigation(self)

        # Main Content Frame
        self.CurrentFrame = None

    def re_translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.Title.setText("Online Voting Signup")

    def reset_current_frame(self):
        if self.CurrentFrame is not None:
            self.CurrentFrame.hide()
            self.CurrentFrame.destroy()

    def ui_start_facilitator(self, page, lang, callback, callback_test):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtStartFacilitator(self, self.config, lang, callback, callback_test)
        self.CurrentFrame.show()

    def ui_start(self, page, participant, lang, callback):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtStart(self, self.config, participant, lang, callback)
        self.CurrentFrame.show()

    def ui_confirm_action(self, page, participant, lang, callback):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtConfirmAction(self, self.config, participant, lang, callback)
        self.CurrentFrame.show()

    def ui_confirm_print(self, page, participant, lang, printed_symbol, callback):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtConfirmPrint(self, self.config, participant, lang, printed_symbol, callback)
        self.CurrentFrame.show()

    def ui_confirm_print_full(self, page, participant, lang, printed_symbol, callback):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtConfirmPrintFull(self, self.config, participant, lang, printed_symbol, callback)
        self.CurrentFrame.show()

    def ui_confirm_print_selection(self, page, participant, lang, correct_symbol,
                                   correct_callback, incorrect_callback):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtConfirmPrintSelection(self, self.config, participant, lang, correct_symbol,
                                                    correct_callback, incorrect_callback)
        self.CurrentFrame.show()

    def ui_confirm_status(self, page, participant, lang, callback):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtConfirmStatus(self, self.config, participant, lang, callback)
        self.CurrentFrame.show()

    def ui_choose_action(self, page, participant, lang, callback_left, callback_right):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtChooseAction(self, self.config, participant, lang, callback_left, callback_right)
        self.CurrentFrame.show()

    def ui_scan_qr_code(self, page, participant, lang):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtScanQRCode(self, self.config, participant, lang)
        self.CurrentFrame.show()

    def ui_scan_envelope(self, page, participant, lang, printed_symbol):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtScanEnvelope(self, self.config, participant, lang, printed_symbol)
        self.CurrentFrame.show()

    def ui_scan_envelope_error(self, page, participant, lang, incorrect_symbol, correct_symbol, callback):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtScanEnvelopeError(self, self.config, participant, lang, incorrect_symbol, correct_symbol,
                                                callback)
        self.CurrentFrame.show()

    def ui_discard_qr_code(self, page, participant, lang, callback_left, callback_right):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = Qt_Discard_QR_Code(self, self.config, participant, lang, callback_left, callback_right)
        self.CurrentFrame.show()

    def ui_test_credential_create_info(self, page, participant, lang, symbol, callback):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtTestCredentialCreateInfo(self, self.config, participant, lang, symbol, callback)
        self.CurrentFrame.show()

    def ui_2_step_info(self, page, participant, lang, printed_symbol, callback):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = Qt2StepInfo(self, self.config, participant, lang, printed_symbol, callback)
        self.CurrentFrame.show()

    def ui_quiz_single(self, page, participant, lang, callback_top, callback_bottom):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtQuizSingle(self, self.config, participant, lang, callback_top, callback_bottom)
        self.CurrentFrame.show()

    def ui_quiz_multiple(self, page, participant, quiz, lang, callback):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtQuizMultiple(self, self.config, participant, quiz, lang, callback)
        self.CurrentFrame.show()

    def ui_quiz_result(self, page, participant, lang, result, callback):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtQuizResult(self, self.config, participant, lang, result, callback)
        self.CurrentFrame.show()

    def ui_quiz_result_choose(self, page, participant, lang, result, callback_left, callback_right):
        self.reset_current_frame()

        # self.Navigation.setCurrentPage(page)
        self.CurrentFrame = QtQuizResultChoose(self, self.config, participant, lang, result, callback_left,
                                               callback_right)
        self.CurrentFrame.show()
