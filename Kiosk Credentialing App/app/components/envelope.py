from app.components.symbol import Symbol


class Envelope:

    def __init__(self, symbol, challenge):
        self.symbol = symbol
        self.challenge = challenge

    @staticmethod
    def parse(qr_code_data):
        """
        Returns symbol, challenge
        """
        data = qr_code_data.split(',')
        if len(data) != 2:
            raise Exception("Incorrect QR code format")

        if Symbol.convert_number_to_symbol(int(data[0])) is False or int(data[0]) > 2:
            raise Exception("Convert number to symbol problem")

        return Envelope(Symbol.convert_number_to_symbol(int(data[0])), data[1])
