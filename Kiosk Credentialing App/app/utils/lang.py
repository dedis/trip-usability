import json
import re
from importlib import resources
from types import SimpleNamespace


class Lang:
    English = "en"

    def __init__(self, language):
        if language == Lang.English:
            self.c = Lang.load("en.json")

    @staticmethod
    def filter(text, participant=None):
        if participant is None or "[" not in text:
            return text

        test_credential_replace = re.sub("\[(.*?\|.*?)\]",
                                         lambda x: x.group(0).split('|')[0].replace('[',
                                                                                    '') if not participant.ab_test_credentials else
                                         x.group(0).split('|')[1].replace(']', ''),
                                         text)

        malicious_kiosk_replace = re.sub("\[(.*?\$.*?)\]",
                                         lambda x: x.group(0).split('$')[0].replace('[',
                                                                                    '') if not participant.ab_malicious_kiosk else
                                         x.group(0).split('$')[1].replace(']', ''),
                                         test_credential_replace)

        return malicious_kiosk_replace

    @staticmethod
    def load(file):
        with resources.path("resources.lang", file) as data_path:
            with open(data_path) as data_file:
                return json.load(data_file, object_hook=lambda d: SimpleNamespace(**d))
