#!/usr/bin/env python3

import argparse
import atexit
import copy
import os
import threading

from PyQt5 import QtCore
from dotenv import load_dotenv

from app.GUI.qt_application import Application
# from app.components.QR import QR
from app.GUI.qt_navigation import QtNavigation
from app.components.QR import QR
from app.components.credential import Credential
from app.components.envelope import Envelope
from app.components.quiz import Quiz
from app.components.symbol import Symbol
from app.metrics.participant import Participant
from app.peripherals.keystrokes import KeyStrokes
from app.peripherals.printer import Printer
from app.utils.database import Database, database
from app.utils.lang import Lang
from app.utils.logger import get_logger

logger = get_logger(__name__)

class App:
    """Documentation for the App class.

    This class represents an application that manages the workflow of participant check-in and credential creation.
    The class provides various methods to handle different steps of the workflow.

    Attributes:
        config (Config): An instance of the Config class that holds the application configuration.
        lang (Lang): An instance of the Lang class that holds the language settings.
        gui (Application): An instance of the Application class that handles the user interface.
        QR (QR): An instance of the QR class that handles QR code related operations.
        printer (Printer): An instance of the Printer class that handles printing operations.
        group (int): The group of participants.
        stop_threads (bool): A flag to indicate if the threads should be stopped.
        database_thread (Thread): A thread to process the database queue.
        participant (Participant): An instance of the Participant class that represents a participant.
        credential (Credential): An instance of the Credential class that represents a participant's credential.
        current_quiz (Quiz): An instance of the Quiz class that represents the current quiz.
        input_handler (KeyStrokes/IPC): An instance of the input handler class based on the config.input_handler value.
        envelopes (set): A set of scanned envelopes.

    Methods:
        shutdown(): Shuts down the application.
        reset(): Resets the application state.
        test_facilitator(): Executes the test facilitator workflow.
        enable_peripheral_input(callback): Enables peripheral input and checks for events.
        run(): Runs the application.
        start_facilitator(): Starts the facilitator workflow.
        start(participant_data): Starts the workflow for a new participant.
        real_credential_intro(): Shows the introduction page for the real credential workflow.
        real_credential_intro2(): Shows the second introduction page for the real credential workflow.
        real_credential_create_info(): Shows the overview page for creating a real credential.
        real_credential_steps_quiz(): Shows the quiz page for the real credential steps.
        real_credential_steps_quiz_result(result, selected_options): Shows the result page for the real credential steps quiz.
        check_in(): Shows the check-in page for the real credential workflow.
        checked_in(check_in_ticket): Handles the participant check-in process.
        real_credential_first_print(): Shows the first print page for the real credential workflow.
        real_credential_scan_envelope(): Shows the envelope scan page for the real credential workflow.
        real_credential_scan_envelope_error(incorrect_symbol, correct_symbol): Shows the error page for envelope scanning.
        real_credential_second_print(qr_code_data): Handles the second print process for the real credential workflow.
    """
    def __init__(self, cli_args):
        # General App
        self.config = cli_args
        self.lang = Lang(self.config.lang)
        self.group = cli_args.group

        # Interfaces
        self.gui = Application(self.config, self.shutdown)
        self.QR = QR(self.config)
        self.printer = Printer(self.config, self.config.printer_name)

        # Database
        self.stop_threads = False
        if self.config.use_db:
            self.database_thread = threading.Thread(target=database.process_queue, args=(lambda: self.stop_threads,))

        self.participant = None
        self.credential = None
        self.current_quiz = None
        self.input_handler = None
        self.envelopes = set()

        atexit.register(self.shutdown)

    # Utils
    def shutdown(self):
        logger.info("Thread Join")
        self.stop_threads = True
        if self.config.use_db:
            self.database_thread.join()

        if self.participant is not None:
            self.participant.close_previous_page()
            self.participant.save()
            self.reset()

    def reset(self):
        self.participant = None
        self.credential = None
        self.current_quiz = None
        self.input_handler = None
        self.envelopes = set()

    def test_facilitator(self):
        logger.info("----- Test Facilitator -----")
        self.printer.print_test_page()

    def enable_peripheral_input(self, callback):
        self.input_handler = KeyStrokes(callback)

        QtCore.QTimer.singleShot(100, lambda: self.input_handler.check_for_event())

    # Start of Application Workflow
    def run(self):
        if self.config.use_db:
            self.database_thread.start()

        test_credentials = 1
        malicious_kiosk = 0
        security_priming = 0
        if self.group == 1:
            test_credentials = 0
        elif self.group == 3:
            malicious_kiosk = 1

        self.start((100001, self.group, test_credentials, malicious_kiosk, security_priming))
        logger.info("Print Test Page")
        self.printer.print_test_page()
        self.gui.run()

    def start_facilitator(self):
        logger.info("----- Start Facilitator -----")
        self.gui.ui_start_facilitator(QtNavigation.NONE, self.lang.c.StartFacilitator, self.start,
                                      self.test_facilitator)

    def start(self, participant_data):
        logger.info("[New Participant]: " + str(participant_data))
        if self.participant is not None:
            self.participant.close_previous_page()
            self.participant.save()
            self.reset()

        self.participant = Participant()
        self.participant.setup(participant_data)
        self.participant.open_page(self.start.__name__)

        self.gui.ui_start(QtNavigation.CHECKIN, self.participant, self.lang.c.Start,
                          self.real_credential_intro)

    def real_credential_intro(self):
        logger.info("[Real Credential] Introduction Page 1")
        self.participant.open_page(self.real_credential_intro.__name__)

        # GUI
        self.gui.ui_confirm_action(QtNavigation.CREDENTIAL, self.participant, self.lang.c.RealCredentialIntro,
                                   self.real_credential_intro2)

    def real_credential_intro2(self):
        logger.info("[Real Credential] Introduction Page 2")
        self.participant.open_page(self.real_credential_intro2.__name__)

        # Control Flow: Malicious or Normal
        if self.participant.ab_malicious_kiosk:
            cred_type = Credential.FAKE_REAL
            callback = self.check_in
        else:
            cred_type = Credential.REAL
            callback = self.real_credential_create_info

        self.credential = Credential(self.participant, cred_type, Symbol.get_random_symbol())

        # GUI
        self.gui.ui_choose_action(QtNavigation.CREDENTIAL, self.participant, self.lang.c.RealCredentialIntro2,
                                  self.real_credential_intro, callback)

    def real_credential_create_info(self):
        logger.info("[Real Credential] Create Credential Overview")
        self.participant.open_page(self.real_credential_create_info.__name__)

        # GUI
        self.gui.ui_real_credential_create_info(QtNavigation.CREDENTIAL, self.participant,
                                                self.lang.c.RealCredentialCreateInfo, self.credential.display_symbol,
                                                self.real_credential_intro2, self.real_credential_steps_quiz)

    def real_credential_steps_quiz(self):
        logger.info("[Real Credential] Steps Quiz")
        self.participant.open_page(self.real_credential_steps_quiz.__name__)

        if self.current_quiz is None:
            self.current_quiz = Quiz(Quiz.REAL_CREDENTIAL_STEPS, self.participant,
                                     self.lang.c.RealCredentialStepsQuiz.Options,
                                     self.lang.c.RealCredentialStepsQuiz.CorrectOptions)

        self.gui.ui_quiz_multiple(QtNavigation.CREDENTIAL, self.participant, self.current_quiz,
                                  self.lang.c.RealCredentialStepsQuiz, self.real_credential_steps_quiz_result)

    def real_credential_steps_quiz_result(self, result, selected_options):
        logger.info("[Real Credential] Steps Quiz|Result: " + result + "|Selected Options: " + str(selected_options))
        self.participant.open_page(self.real_credential_steps_quiz_result.__name__)

        # Save Quiz Response
        self.current_quiz.save(result, selected_options)

        if self.current_quiz.proceed(result):
            callback = self.check_in
            self.current_quiz = None
        else:
            callback = self.real_credential_create_info

        self.gui.ui_quiz_result(QtNavigation.CREDENTIAL, self.participant, self.lang.c.RealCredentialStepsQuizResult,
                                result, callback)

    def check_in(self):
        logger.info("[Real Credential] Check-In")
        self.participant.open_page(self.check_in.__name__)

        self.enable_peripheral_input(self.checked_in)
        self.gui.ui_scan_qr_code(QtNavigation.CHECKIN, self.participant, self.lang.c.CheckIn,
                                 self.input_handler)

    def checked_in(self, check_in_ticket):
        logger.info("[Real Credential] Checked In| Check-In Ticket: " + str(check_in_ticket))

        # Validate Check-In Ticket content
        try:
            if self.participant.validate_check_in_ticket(check_in_ticket) is False:
                database.add_to_queue(Database.LOG, {
                    "log": Database.ERROR,
                    "message": "Check-In Ticket Issue:" + str(check_in_ticket),
                    "participant": copy.deepcopy(self.participant)
                })

        except Exception as e:
            logger.info(str(Database.ERROR) + ": Check-In Ticket Issue: " + str(e) + ":" + str(check_in_ticket) +
                        str(self.participant))

        if self.participant.ab_malicious_kiosk:
            self.real_credential_scan_envelope()
            return

        self.real_credential_first_print()

    def real_credential_first_print(self):
        logger.info("[Real Credential] First Print")
        self.participant.open_page(self.real_credential_first_print.__name__)

        # Print Symbol & QR Code
        self.credential.print_commit(self.credential.display_symbol, self.printer)

        # Confirm Printing
        self.gui.ui_confirm_print(QtNavigation.CREDENTIAL, self.participant,
                                  self.lang.c.RealCredentialFirstPrint,
                                  self.credential.display_symbol, self.real_credential_scan_envelope)

    def real_credential_scan_envelope(self):
        logger.info("[Real Credential] Scan Envelope")
        self.participant.open_page(self.real_credential_scan_envelope.__name__)

        self.enable_peripheral_input(self.real_credential_second_print)
        self.gui.ui_scan_envelope(QtNavigation.CREDENTIAL, self.participant, self.lang.c.RealCredentialScanEnvelope,
                                  self.credential.display_symbol, self.input_handler)

    def real_credential_scan_envelope_error(self, incorrect_symbol, correct_symbol):
        logger.info("[Real Credential] Scan Envelope Error")
        self.participant.open_page(self.real_credential_scan_envelope_error.__name__)

        self.credential.scan_until_correct += 1

        self.gui.ui_scan_envelope_error(QtNavigation.CREDENTIAL, self.participant,
                                        self.lang.c.RealCredentialScanEnvelopeError,
                                        incorrect_symbol, correct_symbol,
                                        self.real_credential_scan_envelope)

    def real_credential_second_print(self, qr_code_data):
        logger.info("[Real Credential] Second Print | QR Code: " + str(qr_code_data))
        self.participant.open_page(self.real_credential_second_print.__name__)

        try:
            envelope = Envelope.parse(qr_code_data)
            if envelope.challenge in self.envelopes:
                self.real_credential_scan_envelope()
                return
        except Exception as e:
            logger.error("Envelope parsing: " + str(e))
            Database.log(Database.ERROR, "Envelope parsing: " + str(e) + ":" + str(qr_code_data), self.participant)
            self.real_credential_scan_envelope()
            return

        if self.participant.ab_malicious_kiosk:
            self.credential.print_commit(envelope.symbol, self.printer)
        elif self.credential.display_symbol != envelope.symbol:
            self.real_credential_scan_envelope_error(envelope.symbol, self.credential.display_symbol)
            return

        self.credential.combine_with_envelope(envelope)
        self.envelopes.add(envelope.challenge)
        self.credential.print_check_out(self.config, self.printer)
        self.credential.print_response(self.printer)

        callback = self.real_credential_confirm_full if not self.participant.ab_malicious_kiosk else self.real_credential_finalize
        self.printer.check_job(callback)

    def real_credential_confirm_full(self):
        logger.info("[Real Credential] Confirm Full")
        self.participant.open_page(self.real_credential_confirm_full.__name__)

        self.gui.ui_confirm_print_full(QtNavigation.CREDENTIAL, self.participant,
                                       self.lang.c.RealCredentialSecondPrint,
                                       self.credential.display_symbol,
                                       self.real_credential_finalize)

    def real_credential_finalize(self):
        logger.info("[Real Credential] Finalize")
        self.participant.open_page(self.real_credential_finalize.__name__)

        self.gui.ui_2_step_info(QtNavigation.CREDENTIAL, self.participant, self.lang.c.RealCredentialFinalize,
                                self.credential.display_symbol, self.real_credential_success)

    def real_credential_success(self):
        logger.info("[Real Credential] Mark")
        self.participant.open_page(self.real_credential_success.__name__)

        # Save Credential
        self.credential.save()

        self.gui.ui_choose_action(QtNavigation.CREDENTIAL, self.participant, self.lang.c.RealCredentialSuccess,
                                  self.real_credential_finalize, self.discard_check_in_ticket)

    def discard_check_in_ticket(self):
        logger.info("Discard Check-In Ticket")
        self.participant.open_page(self.discard_check_in_ticket.__name__)

        self.gui.ui_discard_qr_code(QtNavigation.CHECKIN, self.participant, self.lang.c.DiscardCheckInTicket,
                                    self.real_credential_success, self.real_credential_storage_quiz)

    def real_credential_storage_quiz(self):
        logger.info("[Real Credential] Storage Quiz")
        self.participant.open_page(self.real_credential_storage_quiz.__name__)

        if self.current_quiz is None:
            self.current_quiz = Quiz(Quiz.REAL_CREDENTIAL_STORAGE, self.participant,
                                     self.lang.c.RealCredentialStorageQuiz.Options,
                                     self.lang.c.RealCredentialStorageQuiz.CorrectOptions)

        self.gui.ui_quiz_multiple(QtNavigation.CREDENTIAL, self.participant, self.current_quiz,
                                  self.lang.c.RealCredentialStorageQuiz, self.real_credential_storage_quiz_result)

    def real_credential_storage_quiz_result(self, result, selected_options):
        logger.info("[Real Credential] Storage Quiz|Result: " + result + "|Selected Options: " + str(selected_options))
        self.participant.open_page(self.real_credential_storage_quiz_result.__name__)

        # Save Quiz Result
        self.current_quiz.save(result, selected_options)

        if self.current_quiz.proceed(result):
            callback = self.coercion_intro
            self.current_quiz = None
        else:
            callback = self.real_credential_storage_quiz

        self.gui.ui_quiz_result(QtNavigation.CREDENTIAL, self.participant, self.lang.c.RealCredentialStorageQuizResult,
                                result, callback)

    def coercion_intro(self):
        logger.info("[Coercion] Intro")
        self.participant.open_page(self.coercion_intro.__name__)

        callback = self.test_credential_intro if self.participant.ab_test_credentials else self.finish
        self.gui.ui_confirm_action(QtNavigation.TEST_CREDENTIAL, self.participant, self.lang.c.CoercionIntro, callback)

    def test_credential_intro(self):
        logger.info("[Test Credential] Intro")
        self.participant.open_page(self.test_credential_intro.__name__)

        self.gui.ui_choose_action(QtNavigation.TEST_CREDENTIAL, self.participant, self.lang.c.TestCredentialIntro,
                                  self.coercion_intro, self.test_credential_usage_quiz)

    def test_credential_usage_quiz(self):
        logger.info("[Test Credential] Usage Quiz")
        self.participant.open_page(self.test_credential_usage_quiz.__name__)

        if self.current_quiz is None:
            self.current_quiz = Quiz(Quiz.TEST_CREDENTIAL_USAGE, self.participant,
                                     self.lang.c.TestCredentialUsageQuiz.Options,
                                     self.lang.c.TestCredentialUsageQuiz.CorrectOptions)

        self.gui.ui_quiz_multiple(QtNavigation.CREDENTIAL, self.participant, self.current_quiz,
                                  self.lang.c.TestCredentialUsageQuiz, self.test_credential_usage_quiz_result)

    def test_credential_usage_quiz_result(self, result, selected_options):
        logger.info("[Real Credential] Steps Quiz|Result: " + result + "|Selected Options: " + str(selected_options))
        self.participant.open_page(self.test_credential_usage_quiz_result.__name__)

        # Save Quiz Response
        self.current_quiz.save(result, selected_options)

        if self.current_quiz.proceed(result):
            callback = self.test_credential_create_question
            self.current_quiz = None
        else:
            callback = self.test_credential_intro

        self.gui.ui_quiz_result(QtNavigation.CREDENTIAL, self.participant, self.lang.c.TestCredentialUsageQuizResult,
                                result, callback)

    def test_credential_create_question(self):
        logger.info("[Test Credential] Create Question")
        self.participant.open_page(self.test_credential_create_question.__name__)

        self.credential = Credential(self.participant, Credential.TEST, Symbol.get_random_symbol())

        callback = self.test_credential_steps if not self.participant.ab_malicious_kiosk else self.test_credential_scan_envelope
        self.gui.ui_choose_action(QtNavigation.CREDENTIAL, self.participant, self.lang.c.TestCredentialCreateQuestion,
                                  self.finish, callback)

    def test_credential_steps(self):
        logger.info("[Test Credential] Steps")
        self.participant.open_page(self.test_credential_intro.__name__)

        self.gui.ui_test_credential_create_info(QtNavigation.TEST_CREDENTIAL, self.participant,
                                                self.lang.c.TestCredentialSteps, self.credential.display_symbol,
                                                self.test_credential_scan_envelope)

    def test_credential_scan_envelope(self):
        logger.info("[Test Credential] Scan Envelope")
        self.participant.open_page(self.test_credential_scan_envelope.__name__)

        self.enable_peripheral_input(self.test_credential_print)
        self.gui.ui_scan_envelope(QtNavigation.TEST_CREDENTIAL, self.participant, self.lang.c.TestCredentialEnvelope,
                                  self.credential.display_symbol, self.input_handler)

    def test_credential_print(self, qr_code_data):
        logger.info("[Test Credential] Print")
        self.participant.open_page(self.test_credential_print.__name__)

        try:
            envelope = Envelope.parse(qr_code_data)
            if envelope is False or envelope.challenge in self.envelopes:
                self.test_credential_scan_envelope()
                return
        except Exception as e:
            logger.error("Envelope parsing: " + str(e))
            Database.log(Database.ERROR, "Envelope parsing: " + str(e) + ":" + str(qr_code_data), self.participant)
            self.test_credential_scan_envelope()
            return

        self.credential.combine_with_envelope(envelope)
        self.envelopes.add(envelope.challenge)

        self.credential.print_commit(self.credential.envelope.symbol, self.printer)
        self.credential.print_check_out(self.config, self.printer)
        self.credential.print_response(self.printer)

        self.printer.check_job(self.test_credential_finalize)

    def test_credential_finalize(self):
        logger.info("[Test Credential] Finalize")
        self.participant.open_page(self.test_credential_finalize.__name__)

        self.credential.save()

        self.gui.ui_2_step_info(QtNavigation.TEST_CREDENTIAL, self.participant, self.lang.c.TestCredentialFinalize,
                                self.credential.envelope.symbol, self.test_credential_success)

    def test_credential_success(self):
        logger.info("[Test Credential] Mark")
        self.participant.open_page(self.test_credential_success.__name__)

        callback = self.test_credential_steps if not self.participant.ab_malicious_kiosk else \
            self.test_credential_scan_envelope

        self.gui.ui_choose_action(QtNavigation.TEST_CREDENTIAL, self.participant, self.lang.c.TestCredentialSuccess,
                                  self.credential_distinguish_quiz, callback)

    def credential_distinguish_quiz(self):
        logger.info("[Credential Distinguish] Quiz")
        self.participant.open_page(self.credential_distinguish_quiz.__name__)

        if self.current_quiz is None:
            self.current_quiz = Quiz(Quiz.CREDENTIAL_DISTINGUISH, self.participant,
                                     self.lang.c.CredentialDistinguishQuiz.Options,
                                     self.lang.c.CredentialDistinguishQuiz.CorrectOptions)

        self.gui.ui_quiz_multiple(QtNavigation.CREDENTIAL, self.participant, self.current_quiz,
                                  self.lang.c.CredentialDistinguishQuiz, self.credential_distinguish_quiz_result)

    def credential_distinguish_quiz_result(self, result, selected_options):
        logger.info("[Credential Distinguish] Quiz Result")
        self.participant.open_page(self.credential_distinguish_quiz_result.__name__)

        # Save Quiz Response
        self.current_quiz.save(result, selected_options)

        if self.current_quiz.proceed(result):
            callback = self.finish_with_test_credentials
            self.current_quiz = None
        else:
            callback = self.credential_distinguish_quiz

        self.gui.ui_quiz_result(QtNavigation.TEST_CREDENTIAL, self.participant,
                                self.lang.c.CredentialDistinguishQuizResult, result, callback)

    def finish(self):
        logger.info("Finish")
        self.participant.open_page(self.finish.__name__)

        self.gui.ui_confirm_action(QtNavigation.TEST_CREDENTIAL, self.participant, self.lang.c.Finish,
                                   self.go_to_check_out_desk)

    def finish_with_test_credentials(self):
        logger.info("Finish w/ Test Credentials")
        self.participant.open_page(self.finish_with_test_credentials.__name__)

        self.gui.ui_confirm_action(QtNavigation.TEST_CREDENTIAL, self.participant, self.lang.c.FinishWithTest,
                                   self.go_to_check_out_desk)

    def go_to_check_out_desk(self):
        logger.info("[Finish] Go To Check-Out Desk")
        self.participant.open_page(self.go_to_check_out_desk.__name__)

        self.gui.ui_confirm_action(QtNavigation.TEST_CREDENTIAL, self.participant, self.lang.c.GoToCheckOutDesk,
                                   self.start_facilitator)


def parse_cli_arguments():
    parser = argparse.ArgumentParser(description='Voting Credential Creation Process')
    # Text
    parser.add_argument('--lang', action='store', default='en', help='Language')
    parser.add_argument('--font', action='store', default='Bitstream Charter', help="Font to use")
    parser.add_argument('--button-timeout', type=int, action='store', default=50, help='Timeout')

    parser.add_argument('--prod', action='store_true', help='Enable Production Mode')
    parser.add_argument('--hardware', action='store_true', help='Enable Hardware')
    parser.add_argument('--fullscreen', action='store_true', help='Full Screen Mode')
    parser.add_argument('--verbose', action='store_true', help='Verbose')
    parser.add_argument('--video-source', action='store', default=0, help="Camera Video Source")
    parser.add_argument('--tk-wrap-length-short', action='store', default=315, help='Wrap Length Short')
    parser.add_argument('--tk-wrap-length-long', action='store', default=500, help='Wrap Length Long')
    parser.add_argument('--group', action='store', help='For testing purposes, group number')

    # Scanner
    parser.add_argument('--input_handler', action='store', help='Scanner Input')

    # Printer
    parser.add_argument('--use_printer', action='store_true', help='Enable Printer', default=True)
    parser.add_argument('--printer-name', action='store', help='Printer Name')

    return parser.parse_args()


def load_environment_variables(parser_args):
    load_dotenv()

    # Language
    parser_args.lang = os.getenv('LANG', 'en')

    # Scanner
    parser_args.input_handler = os.getenv('INPUT_HANDLER', 'keystrokes')

    # Printer
    parser_args.use_printer = os.getenv('USE_PRINTER', "false").lower() == 'true'
    parser_args.printer_name = os.getenv('PRINTER_NAME', "TM")

    # Checkout
    parser_args.checkout_url = os.getenv('CHECKOUT_URL', "URL/")
    parser_args.checkout_path = os.getenv('CHECKOUT_PATH', "PATH/")

    # Button
    parser_args.button_timeout = int(os.getenv('BUTTON_TIMEOUT', '50'))

    # Database
    parser_args.use_db = os.getenv('USE_DB', "false").lower() == 'true'

if __name__ == '__main__':
    args = parse_cli_arguments()
    load_environment_variables(args)
    print(args)
    App(args).run()
