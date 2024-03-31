import sys

from PyQt5 import QtWidgets, QtCore

from app.GUI.qt_window import Window
from app.utils.database import Database


class Application:
    def __init__(self, config, shutdown_callback):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = Window(config, shutdown_callback)
        self.config = config

    def run(self):
        if self.config.fullscreen:
            self.window.showFullScreen()
        else:
            self.window.show()
        sys.exit(self.app.exec_())

    def collect_keystrokes(self, input_handler):
        self.window.input_handler = input_handler
        self.window.showFullScreen()
        sys.exit(self.app.exec_())

    def ui_start_facilitator(self, page, lang, callback, callback_test):
        self.window.ui_start_facilitator(page, lang, callback, callback_test)
        QtCore.QTimer.singleShot(200, lambda: self.network_get_participant(callback))

    def network_get_participant(self, callback):
        participant = Database.get_next_participant()
        if participant:
            callback(participant)
        else:
            QtCore.QTimer.singleShot(500, lambda: self.network_get_participant(callback))

    def ui_start(self, page, participant, lang, callback):
        self.window.ui_start(page, participant, lang, callback)

    def ui_confirm_action(self, page, participant, lang, callback):
        self.window.ui_confirm_action(page, participant, lang, callback)

    def ui_confirm_print(self, page, participant, lang, printed_symbol, callback):
        self.window.ui_confirm_print(page, participant, lang, printed_symbol, callback)

    def ui_confirm_print_full(self, page, participant, lang, printed_symbol, callback):
        self.window.ui_confirm_print_full(page, participant, lang, printed_symbol, callback)

    def ui_confirm_print_selection(self, page, participant, lang, correct_symbol,
                                   correct_callback, incorrect_callback):
        self.window.ui_confirm_print_selection(page, participant, lang, correct_symbol,
                                               correct_callback, incorrect_callback)

    def ui_confirm_status(self, page, participant, lang, callback):
        self.window.ui_confirm_status(page, participant, lang, callback)

    def ui_choose_action(self, page, participant, lang, callback_left, callback_right):
        self.window.ui_choose_action(page, participant, lang, callback_left, callback_right)

    def ui_scan_qr_code(self, page, participant, lang, input_handler):
        self.window.ui_scan_qr_code(page, participant, lang, input_handler)

    def ui_scan_envelope(self, page, participant, lang, printed_symbol, input_handler):
        self.window.ui_scan_envelope(page, participant, lang, printed_symbol, input_handler)

    def ui_scan_envelope_error(self, page, participant, lang, incorrect_symbol, correct_symbol, callback):
        self.window.ui_scan_envelope_error(page, participant, lang, incorrect_symbol, correct_symbol, callback)

    def ui_discard_qr_code(self, page, participant, lang, callback_left, callback_right):
        self.window.ui_discard_qr_code(page, participant, lang, callback_left, callback_right)

    def ui_real_credential_create_info(self, page, participant, lang, symbol, callback_left, callback_right):
        self.window.ui_real_credential_create_info(page, participant, lang, symbol, callback_left, callback_right)

    def ui_test_credential_create_info(self, page, participant, lang, symbol, callback):
        self.window.ui_test_credential_create_info(page, participant, lang, symbol, callback)

    def ui_2_step_info(self, page, participant, lang, printed_symbol, callback):
        self.window.ui_2_step_info(page, participant, lang, printed_symbol, callback)

    def ui_quiz_single(self, page, participant, lang, callback_top, callback_bottom):
        self.window.ui_quiz_single(page, participant, lang, callback_top, callback_bottom)

    def ui_quiz_multiple(self, page, participant, quiz, lang, callback):
        self.window.ui_quiz_multiple(page, participant, quiz, lang, callback)

    def ui_quiz_result(self, page, participant, lang, result, callback):
        self.window.ui_quiz_result(page, participant, lang, result, callback)

    def ui_quiz_result_choose(self, page, participant, lang, result, callback_left, callback_right):
        self.window.ui_quiz_result_choose(page, participant, lang, result, callback_left, callback_right)
