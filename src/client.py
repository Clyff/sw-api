from pymongo import MongoClient

class Client(object):

    def __init__(self):
        conection = MongoClient('localhost', 27017)
        self.db = conection['api_database']