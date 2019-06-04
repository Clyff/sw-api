from pymongo import MongoClient

class Client(object):
    """
    A class used to handle the MongoDB Connection.

    Attributes
    ----------
    db : MongoDB Database
    """

    def __init__(self):
        conection = MongoClient('localhost', 27017)
        self.db = conection['api_database']