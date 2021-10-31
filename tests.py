import unittest
import bson
from mongodb_manager import MondoClientManager, MongoClient


class MongoManagerTestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.__connection = MongoClient('localhost', 27017)
        cls.__db = cls.__connection.get_database(
            'TelegramBotDB',
            bson.codec_options.CodecOptions(uuid_representation=bson.binary.UUID_SUBTYPE)
        )

        cls.__collection = cls.__db.TestPhilosophers
        cls.__collection.insert_one(
            {
                'name': 'Філософи',
                'philosophers': []
            }
        )

        cls.__mongoClient = MondoClientManager()
        cls.__mongoClient.database_collection = cls.__collection

    @classmethod
    def tearDownClass(cls) -> None:
        cls.__collection.drop()
        cls.__connection.close()

    def test_add_new_philosopher(self):
        philosopher = 'Сократ'
        self.__mongoClient.add_new_philosopher(philosopher)
        philosophers = self.__mongoClient.get_philosophers_collection()

        self.assertTrue(philosopher in philosophers, 'Required philosopher was not found!')

    def test_insert_quotes_array(self):
        quotes = [
            'Будьте тим, ким хочете бути.',
            'Заговори, щоб я тебе побачив.'
        ]

        self.__mongoClient.insert_quotes_array('Сократ', quotes)
        quote = self.__mongoClient.get_quote('Сократ')
        substrings = quote.split('"')

        result = False
        for str in substrings:
            if str in quotes:
                result = True
                break

        self.assertTrue(result, 'Quote was not found!')
