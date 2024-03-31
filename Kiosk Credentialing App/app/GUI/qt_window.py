#import cv2
import numpy as np
from PyQt5 import QtWidgets, QtCore

from app.GUI.qt_main_frame import MainFrame
from app.GUI.qt_real_credential_create_info import QtRealCredentialCreateInfo

class Window(QtWidgets.QMainWindow):
    def __init__(self, config, shutdown_callback):
        super(Window, self).__init__(parent=None)
        self.setObjectName("MainWindow")
        self.resize(1920, 1080)
        self.config = config
        self.shutdown_callback = shutdown_callback

        self.MainFrame = MainFrame(self, config)
        self.setCentralWidget(self.MainFrame)
        self.re_translate_ui()
        self.setStyleSheet("QMainWindow {background: \"white\";}")

        #self.thread = VideoThread(self)

        self.input_handler = None
        self.callback = None

    def reset(self):
        if self.centralWidget() != self.MainFrame:
            self.MainFrame = MainFrame(self, self.config)
            self.setCentralWidget(self.MainFrame)

        self.input_handler = None

    def keyPressEvent(self, event):
        # Close Program
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
            self.shutdown_callback()

        # Go to next screen
        if event.key() == 16777236:
            self.callback()
            return

        if self.input_handler is not None:
            self.input_handler.handle_event(event)

    def re_translate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def ui_start_facilitator(self, page, lang, callback, callback_test):
        self.reset()

        self.MainFrame.ui_start_facilitator(page, lang, callback, callback_test)
        self.callback = callback

    def ui_start(self, page, participant, lang, callback):
        self.reset()

        self.MainFrame.ui_start(page, participant, lang, callback)
        self.callback = callback

    def ui_confirm_action(self, page, participant, lang, callback):
        self.reset()

        self.MainFrame.ui_confirm_action(page, participant, lang, callback)
        self.callback = callback

    def ui_confirm_print(self, page, participant, lang, printed_symbol, callback):
        self.reset()

        self.MainFrame.ui_confirm_print(page, participant, lang, printed_symbol, callback)
        self.callback = callback

    def ui_confirm_print_full(self, page, participant, lang, printed_symbol, callback):
        self.reset()

        self.MainFrame.ui_confirm_print_full(page, participant, lang, printed_symbol, callback)
        self.callback = callback

    def ui_confirm_print_selection(self, page, participant, lang, correct_symbol,
                                   correct_callback, incorrect_callback):
        self.reset()

        self.MainFrame.ui_confirm_print_selection(page, participant, lang, correct_symbol,
                                                  correct_callback, incorrect_callback)
        self.callback = correct_callback

    def ui_confirm_status(self, page, participant, lang, callback):
        self.reset()

        self.MainFrame.ui_confirm_status(page, participant, lang, callback)
        self.callback = callback

    def ui_choose_action(self, page, participant, lang, callback_left, callback_right):
        self.reset()

        self.MainFrame.ui_choose_action(page, participant, lang, callback_left, callback_right)
        self.callback = callback_right

    def ui_scan_qr_code(self, page, participant, lang, input_handler):
        self.reset()

        self.input_handler = input_handler
        self.MainFrame.ui_scan_qr_code(page, participant, lang)

    def ui_scan_envelope(self, page, participant, lang, printed_symbol, input_handler):
        self.reset()

        self.input_handler = input_handler
        self.MainFrame.ui_scan_envelope(page, participant, lang, printed_symbol)

    def ui_scan_envelope_error(self, page, participant, lang, incorrect_symbol, correct_symbol, callback):
        self.reset()

        self.MainFrame.ui_scan_envelope_error(page, participant, lang, incorrect_symbol, correct_symbol, callback)
        self.callback = callback

    def ui_discard_qr_code(self, page, participant, lang, callback_left, callback_right):
        self.reset()

        self.MainFrame.ui_discard_qr_code(page, participant, lang, callback_left, callback_right)
        self.callback = callback_right

    def ui_real_credential_create_info(self, page, participant, lang, symbol, callback_left, callback_right):
        self.setCentralWidget(
            QtRealCredentialCreateInfo(self, self.config, participant, lang, symbol, callback_left, callback_right))
        self.show()
        self.callback = callback_right

    def ui_test_credential_create_info(self, page, participant, lang, symbol, callback):
        self.reset()

        self.MainFrame.ui_test_credential_create_info(page, participant, lang, symbol, callback)
        self.callback = callback

    def ui_2_step_info(self, page, participant, lang, printed_symbol, callback):
        self.reset()

        self.MainFrame.ui_2_step_info(page, participant, lang, printed_symbol, callback)
        self.callback = callback

    def ui_quiz_single(self, page, participant, lang, callback_top, callback_bottom):
        self.reset()

        self.MainFrame.ui_quiz_single(page, participant, lang, callback_top, callback_bottom)
        self.callback = callback_bottom

    def ui_quiz_multiple(self, page, participant, quiz, lang, callback):
        self.reset()

        self.MainFrame.ui_quiz_multiple(page, participant, quiz, lang, callback)
        self.callback = callback

    def ui_quiz_result(self, page, participant, lang, result, callback):
        self.reset()

        self.MainFrame.ui_quiz_result(page, participant, lang, result, callback)
        self.callback = callback

    def ui_quiz_result_choose(self, page, participant, lang, result, callback_left, callback_right):
        self.reset()

        self.MainFrame.ui_quiz_result_choose(page, participant, lang, result, callback_left, callback_right)
        self.callback = callback_right
