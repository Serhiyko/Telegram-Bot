import bson
from pymongo import MongoClient

import random


class MondoClientManager:
    def __init__(self):
        self.__connection = MongoClient()
        self.__db= None
        self.__collection = None

    def __del__(self):
        self.__connection.close()

    @property
    def database_collection(self):
        return self.__collection

    @database_collection.setter
    def database_collection(self, value):
        self.__collection = value

    def initialize_connection(self):
        self.__connection = MongoClient('localhost', 27017)
        self.__db = connection.get_database(
            'TelegramBotDB',
            bson.codec_options.CodecOptions(uuid_representation=bson.binary.UUID_SUBTYPE)
        )

        self.__collection = self.__db.Philosophers

    def add_new_philosopher(self, new_name):
        self.__collection.update_one(
            {'name': 'Філософи'},
            {
                '$push': {
                    'philosophers': new_name
                }
            }
        )

    def insert_quotes_array(self, philosopher, quotes):
        self.__collection.insert_one(
            {
                'name': philosopher,
                'quotes': quotes
            }
        )

    def add_new_quote(self, philosopher, quote):
        self.__collection.update_one(
            {'name': philosopher},
            {
                '$push': {
                    'quotes': quote
                }
            }
        )

    def get_philosophers_collection(self):
        result = []

        query = { 'name': 'Філософи' }
        main_catalog = self.__collection.find(query)
        for item in main_catalog:
            result.extend(item['philosophers'])

        return result

    def get_quote(self, philosopher):
        quotes = []

        query = { 'name': philosopher }
        required_catalog = self.__collection.find(query)

        for item in required_catalog:
            quotes.extend(item['quotes'])

        if len(quotes) == 0:
            return "Quote was not found ({})".format(philosopher)

        quote = "\"{}\" ({})".format(random.choice(quotes), philosopher)
        return quote

    def get_random_quote(self):
        philosophers = self.get_philosophers_collection()
        philosopher = random.choice(philosophers)

        return  self.get_quote(philosopher)
