import secrets

from importlib import resources
from app.utils.logger import get_logger

logger = get_logger(__name__)

class Symbol:
    SQUARE = "square"
    SQUARE_NO = 0
    CIRCLE = "circle"
    CIRCLE_NO = 1
    TRIANGLE = "triangle"
    TRIANGLE_NO = 2

    CORRECT_SYMBOL = "Correct Symbol"
    INCORRECT_SYMBOL = "Incorrect Symbol"

    @staticmethod
    def get_path(symbol):
        with resources.path("app.resources.images.user_challenge", symbol + ".png") as data_path:
            return str(data_path.absolute())

    @staticmethod
    def get_random_symbol():
        # return Symbol.convert_number_to_symbol(2)
        random_int = secrets.randbelow(3)
        return Symbol.convert_number_to_symbol(random_int)

    @staticmethod
    def convert_number_to_symbol(symbol_number):
        if symbol_number == Symbol.SQUARE_NO:
            return Symbol.SQUARE
        elif symbol_number == Symbol.CIRCLE_NO:
            return Symbol.CIRCLE

        return Symbol.TRIANGLE

    @staticmethod
    def get_unicode_symbol(symbol):
        if symbol == Symbol.SQUARE:
            return "\u25A0"
        elif symbol == Symbol.CIRCLE:
            return "\u25CF"

        return "\u25B2"
