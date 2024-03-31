import os

from app.components.QR import QR
from app.components.bar import Bar


PATH='resources/codes/'

def generate_check_in_ticket(start, end):
    index = start

    check_in_path = os.path.join(PATH, 'checkin')
    if not os.path.exists(check_in_path):
        os.mkdir(check_in_path)

    while index < end:
        Bar.create(os.path.join(check_in_path, str(index)), str(index))
        index += 1


def generate_envelopes(start, end, symbols):
    index = start

    envelope_path = os.path.join(PATH, 'envelopes')
    if not os.path.exists(envelope_path):
        os.mkdir(envelope_path)

    while index < end:
        result = index % len(symbols)
        qr_code = QR.generate_qr(str(result) + "," + str(index))
        qr_code.save(os.path.join(envelope_path, str(index) + ".svg"))
        index += 1


if __name__ == '__main__':
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    generate_check_in_ticket(12110, 12250)
    generate_envelopes(10000000000000001000, 10000000000000001200, ['square', 'circle', 'triangle'])
