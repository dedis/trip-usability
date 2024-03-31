import json
import os
from datetime import datetime, timedelta

from app.utils.logger import get_logger

logger = get_logger(__name__)


def convert_to_json(o):
    if isinstance(o, datetime):
        return o.__str__()
    elif isinstance(o, timedelta):
        return o.__str__()


class Participant:
    def __init__(self, check_in_id=-1, group=-1, test_credentials=False, malicious_kiosk=False, security_priming=False):
        # Check-In Data
        self.check_in_id = check_in_id
        self.group = group
        self.ab_test_credentials = test_credentials
        self.ab_malicious_kiosk = malicious_kiosk
        self.ab_security_priming = security_priming

        # Credential Data
        self.credentials = {}

        # Quizzes Data
        self.quizzes = {}

        # Pages Data
        self.pages = {}
        self.last_page = None
        self.page_increment = 0

        # File Backup
        self.filename = None

    def setup(self, data):
        (check_in_id, group, test_credentials, malicious_kiosk, security_priming) = data
        # Load Participant Information
        self.check_in_id = int(check_in_id)
        self.group = int(group)
        self.ab_test_credentials = True if test_credentials == 1 else False
        self.ab_malicious_kiosk = True if malicious_kiosk == 1 else False
        self.ab_security_priming = True if security_priming == 1 else False

        logger.info('ID: ' + str(self.check_in_id) +
                    ' |Group: ' + str(self.group) +
                    ' |Test Credentials: ' + str(self.ab_test_credentials) +
                    ' |Malicious Kiosk: ' + str(self.ab_malicious_kiosk) +
                    ' |Security Priming: ' + str(self.ab_security_priming))

        self.filename = str(int(datetime.now().timestamp())) + '_' + str(self.check_in_id)

        assert 0 < self.check_in_id < 2147483647
        assert 0 < self.group < 100

    def validate_check_in_ticket(self, check_in_id):
        """
        Ensures that the check-in ticket's contents corresponds with the set data.
        """
        if int(check_in_id) != self.check_in_id:
            return False

        return True

    def set_quiz_result(self, name, result, selected_options):
        if name not in self.quizzes:
            self.quizzes[name] = []

        data = (result, str(selected_options), datetime.now())
        self.quizzes[name].append(data)

    def add_credential(self, credential):
        if credential.type not in self.credentials:
            self.credentials[credential.type] = []

        data = (credential.envelope.challenge, credential.type, credential.display_symbol, credential.envelope.symbol,
                credential.scan_until_correct, datetime.now())
        self.credentials[credential.type].append(data)

    def open_page(self, page):
        # if another page is open, close and reset
        if self.last_page is not None:
            self.close_previous_page()
            self.save()

        self.page_increment = 0
        if page not in self.pages:
            self.pages[page] = [{'index': self.page_increment}]
        else:
            self.page_increment = len(self.pages[page])
            self.pages[page].append({'index': self.page_increment})

        self.pages[page][self.page_increment]['start'] = datetime.now()
        self.last_page = page

    def close_previous_page(self):
        self.pages[self.last_page][self.page_increment]['end'] = datetime.now()
        self.pages[self.last_page][self.page_increment]['length'] = \
            self.pages[self.last_page][self.page_increment]['end'] - \
            self.pages[self.last_page][self.page_increment]['start']

        self.last_page = None
        self.page_increment = 0

    def calculate_total_time(self):
        if 'check_in' in self.pages and 'finish' in self.pages and 'end' in self.pages['finish'][0]:
            total_time = self.pages['finish'][0]['end'] - self.pages['start'][0]['start']
        elif 'check_in' in self.pages and 'finish_with_test_credentials' in self.pages and 'end' in \
                self.pages['finish_with_test_credentials'][0]:
            total_time = self.pages['finish_with_test_credentials'][0]['end'] - self.pages['check_in'][0]['start']
        else:
            total_time = None

        return total_time

    def save(self):
        # Calculations
        total_time = self.calculate_total_time()

        json_data = {
            'id': self.check_in_id,
            'group': self.group,
            'ab_test_credentials': self.ab_test_credentials,
            'ab_malicious_kiosk': self.ab_malicious_kiosk,
            'ab_security_priming': self.ab_security_priming,
            'credentials': self.credentials,
            'quizzes': self.quizzes,
            'pages': self.pages,
            'total_time': total_time
        }

        if not os.path.exists("participants"):
            os.makedirs("participants")

        with open(os.path.join('participants/', self.filename), 'w') as outfile:
            json.dump(json_data, outfile, default=convert_to_json, indent=4)
