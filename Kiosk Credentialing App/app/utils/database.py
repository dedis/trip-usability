import datetime
import queue
import os

from app.utils.logger import get_logger

# import mysql.connector

logger = get_logger(__name__)

USE_DB = os.getenv('USE_DB', "false").lower() == 'true'
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

class Database:
    WARNING = 2
    ERROR = 1

    QUIZ_RESULT = "QuizResult"
    SAVE_CREDENTIAL = "SaveCredential"
    LOG = "Log"

    def __init__(self):
        if not USE_DB:
            return

        self.mydb = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )

        self.queue = queue.Queue()

    def add_to_queue(self, method, args):
        if not USE_DB:
            return
        
        self.queue.put([method, args])

    def process_queue(self, stop):
        while True:
            try:
                if stop():
                    break
                (method, args) = self.queue.get(timeout=5)

                if method == Database.QUIZ_RESULT:
                    Database.save_quiz_result(args["participant"], args["quiz"], args["result"],
                                              args["selected_options"])
                elif method == Database.SAVE_CREDENTIAL:
                    Database.save_credential(args["credential"])
                elif method == Database.LOG:
                    if "participant" in args:
                        Database.log(args["log"], args["message"], args["participant"])
                    else:
                        Database.log(args["log"], args["message"])
            except TimeoutError as e:
                logger.debug("Timeout")
            except Exception as e:
                # logger.error("Database Thread Fatal Exception Occurred: " + str(e))
                pass

    @staticmethod
    def get_next_participant():
        """
        Returns (check_in_id, group_id, test_credentials, kiosk_malicious, security_priming)
        """
        db = Database()
        if not USE_DB:
            return

        cursor = db.mydb.cursor()

        cursor.execute(
            "SELECT participants.id, groups.id, test_credentials, kiosk_malicious, security_priming "
            "FROM participants LEFT JOIN groups ON participants.group_id = groups.id WHERE kiosk_setup_at IS NULL "
            "ORDER BY created_at DESC LIMIT 0,1")

        result = cursor.fetchall()

        if len(result) == 1:
            now = datetime.datetime.utcnow()
            cursor.execute("UPDATE participants SET kiosk_setup_at = %s WHERE id = %s",
                           (now.strftime('%Y-%m-%d %H:%M:%S'), result[0][0]))
            db.mydb.commit()
            db.mydb.close()
            return result[0]

        db.mydb.close()
        return False

    @staticmethod
    def save_quiz_result(participant, quiz, result, selected_options):
        try:
            db = Database()
            if not USE_DB:
                return

            cursor = db.mydb.cursor()

            cursor.execute(
                "INSERT INTO quiz_results(participant_id, quiz_id, correct, selected_options) VALUES(%s, %s, %s, %s)",
                (str(participant.check_in_id), str(quiz.type), str(result), str(list(selected_options)))
            )

            db.mydb.commit()

        except Exception as e:
            logger.error("Unable to access the database to save quiz information: " + str(e) + ":" +
                         str(participant.check_in_id) + ":" + str(quiz.type) + ":" + str(result) + ":" +
                         str(list(selected_options)))

    @staticmethod
    def save_credential(credential):
        try:
            db = Database()
            if not USE_DB:
                return

            cursor = db.mydb.cursor()

            cursor.execute(
                "INSERT INTO credentials (participant_id, envelope_id, cred_type, display_symbol, envelope_symbol, scan_until_correct) VALUES (%s, %s, %s, %s, %s, %s)",
                (credential.participant.check_in_id, credential.envelope.challenge, credential.type,
                 credential.display_symbol, credential.envelope.symbol, credential.scan_until_correct))
            db.mydb.commit()

        except Exception as e:
            logger.error(
                "Unable to access the database to save credential information: " + str(e) + ":" +
                str(credential.participant.check_in_id) + ":" + str(credential.envelope.challenge) + ":" +
                str(credential.type) + ":" + str(credential.display_symbol) + ":" + str(credential.envelope.symbol) +
                ":" + str(credential.scan_until_correct))

    @staticmethod
    def log(level, message, participant=None):
        try:
            db = Database()
            if not USE_DB:
                return

            cursor = db.mydb.cursor()

            participant_id = participant.check_in_id if participant is not None else None

            cursor.execute("INSERT INTO logs (participant_id, level, message) VALUES (%s, %s, %s)",
                           (participant_id, level, message))

            db.mydb.commit()

        except Exception as e:
            logger.error(
                "Unable to access the database to save log information: " + str(e) + ":" + str(level) + ":" +
                str(message))


database = Database()
