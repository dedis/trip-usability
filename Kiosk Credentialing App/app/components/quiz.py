import copy
import random

from app.utils.database import Database, database


class Quiz:
    REAL_CREDENTIAL_STEPS = "real_credential_steps"
    REAL_CREDENTIAL_STORAGE = "real_credential_storage"
    TEST_CREDENTIAL_USAGE = "test_credential_usage"
    CREDENTIAL_DISTINGUISH = "credential_distinguish"

    CORRECT = "Correct"
    INCORRECT = "Incorrect"

    def __init__(self, type, participant, options, correct_options):
        self.type = type
        self.participant = participant
        self.options = list(options)
        random.shuffle(self.options)
        self.correct_options = correct_options
        self.attempts = 0

    def save(self, result, selected_options):
        self.participant.set_quiz_result(self.type, result, list(selected_options))
        result = 1 if result == Quiz.CORRECT else 0
        database.add_to_queue(Database.QUIZ_RESULT, {
            "participant": copy.deepcopy(self.participant),
            "quiz": copy.deepcopy(self),
            "result": copy.deepcopy(result),
            "selected_options": list(selected_options)
        })
        self.attempts += 1

    def proceed(self, result):
        return result == Quiz.CORRECT or self.attempts >= 3
