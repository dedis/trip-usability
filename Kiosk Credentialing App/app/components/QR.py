import random

import segno

from app.utils.logger import get_logger

logger = get_logger(__name__)


class QR:
    KIOSK_ID = 1

    def __init__(self, config):  # gui: Window, camera: Camera):
        self.config = config

    @staticmethod
    def generate_random_qr():
        rand = random.random()
        return segno.make_qr(str(rand) + str(rand) + str(rand))

    @staticmethod
    def generate_qr(data):
        return segno.make_qr(data, error="M")

    @staticmethod
    def generate_commit_qr(participant, credential_type):
        return segno.make_qr(str(QR.KIOSK_ID) + "," +
                             str(participant.check_in_id) + "," +
                             str(participant.group) + "," +
                             str(credential_type))

    @staticmethod
    def generate_check_out_qr(config, participant, envelope, credential_type):
        return segno.make_qr(config.checkout_url + config.checkout_path +
                             "?kk=" + str(QR.KIOSK_ID) +
                             "&id=" + str(participant.check_in_id) +
                             "&group=" + str(participant.group) +
                             "&symbol=" + str(envelope.symbol) +
                             "&ch=" + str(envelope.challenge) +
                             "&cred=" + str(credential_type))

    @staticmethod
    def generate_response_qr(participant, envelope):
        return segno.make_qr(str(QR.KIOSK_ID) + "," +
                             str(participant.check_in_id) + "," +
                             str(envelope.challenge))
