import copy

from app.components.QR import QR
from app.utils.database import Database, database


class Credential:
    REAL = "real"
    FAKE_REAL = "fake_real"
    TEST = "test"

    def __init__(self, participant, type, display_symbol):
        self.participant = participant
        self.display_symbol = display_symbol
        self.type = type
        self.scan_until_correct = 0
        self.envelope = None

    def combine_with_envelope(self, envelope):
        self.envelope = envelope

    def print_commit(self, symbol, printer):
        printer.print_symbol(symbol, bot_reduction=True, top_reduction=True)
        qr_1 = QR.generate_commit_qr(self.participant, self.type)
        printer.print_qr(qr_1, page_width=43, top_reduction=True)

    def print_check_out(self, config, printer):
        qr_2 = QR.generate_check_out_qr(config, self.participant, self.envelope, self.type)
        printer.print_qr(qr_2, bot_reduction=True)
        printer.print_white(page_width=20, page_height=20)

    def print_response(self, printer):
        qr_3 = QR.generate_response_qr(self.participant, self.envelope)
        printer.print_qr(qr_3, top_reduction=True, bot_reduction=True)
        printer.print_arrow()

    def save(self):
        self.participant.add_credential(self)
        database.add_to_queue(Database.SAVE_CREDENTIAL, {
            "credential": copy.deepcopy(self),
        })
