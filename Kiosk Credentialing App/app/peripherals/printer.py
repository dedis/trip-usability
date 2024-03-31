import tempfile
import time
from importlib import resources

import cups

from app.components.symbol import Symbol
from app.utils.logger import get_logger

logger = get_logger(__name__)

ARROW = "arrow.jpg"
WHITE = "white.png"


class Printer:
    def __init__(self, config, printer_host=None, printer_name=None):
        self.config = config

        self.conn = cups.Connection()
        self.jobs = []
        self.files = []

        if printer_name is None:
            printers = self.conn.getPrinters()
            printer_name = list(printers.keys())[0]

        cups.setUser('linaro')
        self.printer_name = printer_name

    def print_test_page(self):
        self.print_symbol(Symbol.get_random_symbol(), cut=True, top_reduction=False, bot_reduction=True)

    def print_qr(self, code, page_width=48, cut=False, top_reduction=False, bot_reduction=False):
        output_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
        code.save(output_file)
        logger.info("Path for temp image: " + output_file)

        self.print(output_file, page_width=page_width, cut=cut, top_reduction=top_reduction,
                   bot_reduction=bot_reduction)

    def print_arrow(self):
        with resources.path("app.resources.images", ARROW) as data_path:
            self.print(str(data_path.absolute()), cut=True, top_reduction=True, bot_reduction=True)

    def print_symbol(self, symbol, cut=False, top_reduction=False, bot_reduction=False):
        self.print(Symbol.get_path(symbol), page_width=48, page_height=43, cut=cut, top_reduction=top_reduction,
                   bot_reduction=bot_reduction)

    def print_white(self, page_width=48, page_height=48, cut=False):
        with resources.path("app.resources.images", WHITE) as data_path:
            self.print(str(data_path.absolute()), page_width=page_width, page_height=page_height,
                       cut=cut, top_reduction=False, bot_reduction=False)

    def print(self, file, page_width=48, page_height=200, cut=False, top_reduction=False, bot_reduction=False):
        # Print output
        self.files.append(file)

        if self.config.prod is False:
            logger.debug("printing (Sim): Job sent to printer: ", file)
            return

        options = {"PageSize": "Custom." + str(page_width) + "x" + str(
            page_height) + "mm"}  # {"PageSize": "Custom.48x200mm", "TmxPaperCut": "CutPerPage"}
        if cut is not False:
            options["TmxPaperCut"] = "CutPerPage"
        if top_reduction and bot_reduction:
            options["TmxPaperReduction"] = "Both"
        elif top_reduction:
            options["TmxPaperReduction"] = "Top"
        elif bot_reduction:
            options["TmxPaperReduction"] = "Bottom"

        logger.info(str(file))
        logger.info(str(self.printer_name))
        # job_id = self.conn.printFile(self.printer_name, file, "QRCode", options)
        # self.jobs.append(job_id)
        # logger.debug("Printing: Job ID: ", self.jobs)
        # return
        while True:
            try:
                job_id = self.conn.printFile(self.printer_name, file, "QRCode", options)
                self.jobs.append(job_id)
                logger.debug("Printing: Job ID: ", self.jobs)
                break
            except Exception as e:
                logger.error("Printer Error: " + str(e))
                time.sleep(0.5)

    def debug_print(self, code=None, file=None, page_size=48, page_size_2=200, reduction="Both"):
        if code is not None:
            output_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
            print(output_file)
            code.save(output_file)
            logger.info("Path for temp image: " + str(output_file))
        elif file == 1:
            with resources.path("app.resources.images.user_challenge", "square.png") as data_path:
                output_file = str(data_path.absolute())
        elif file == 2:
            with resources.path("app.resources.images", "white.png") as data_path:
                output_file = str(data_path.absolute())

        print(output_file)
        return

        options = {}  # {"PageSize": "Custom.48x300mm", "TmxPaperCut": "CutPerJob"}
        options["PageSize"] = "Custom." + str(page_size) + "x" + str(page_size_2) + "mm"
        options["TmxPaperReduction"] = reduction

        while True:
            try:
                self.conn.printFile(self.printer_name, output_file, "QRCode", options)
                break
            except Exception as e:
                logger.error("Printer Error: " + str(e))
                time.sleep(0.5)

    def check_job(self, callback):
        if self.config.prod is False:
            time.sleep(0.5 * len(self.files))
            self.files.clear()
            logger.debug("Printing (Sim): Job Done")
            callback()
            return

        while len(self.jobs) > 0:
            job_id = self.jobs.pop()
            file = self.files.pop()

            while self.conn.getJobs().get(job_id, None):
                time.sleep(1)

            # os.unlink(file)

            logger.debug("Printing: Job ", job_id, " Done")

        callback()


class PrinterMimic:
    def __init__(self, config, printer_name=None):
        pass

    def print_qr(self, code, cut=False, top_reduction=False):
        pass

    def arrow(self):
        pass

    def print(self, file, page_size=None, cut=False, top_reduction=False):
        pass

    def check_job(self, callback):
        pass
