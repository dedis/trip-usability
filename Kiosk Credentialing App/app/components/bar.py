from barcode import Code128
from barcode.writer import SVGWriter


class Bar:
    @staticmethod
    def create(file, data):
        with open(file, "wb") as f:
            Code128(str(data), writer=SVGWriter()).write(f)
