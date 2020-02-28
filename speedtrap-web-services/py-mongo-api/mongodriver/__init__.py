import os
from pymongo import MongoClient
import urllib

class MongoDriver:

    def __init__(self):
        
        with open(os.environ['MONGO_USERNAME'], 'r') as user_secret:
            self.mongo_username = user_secret.read().strip()

        with open(os.environ['MONGO_PASSWORD'], 'r') as pass_secret:
            self.mongo_password = pass_secret.read().strip()

    def db_connection(self, host, database):

        client = MongoClient('mongodb://%s:%s@%s/%s' % (self.mongo_username, self.mongo_password, host, database))

        return client
