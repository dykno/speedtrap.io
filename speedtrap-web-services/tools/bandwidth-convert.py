from bson.objectid import ObjectId
import os
from pymongo import MongoClient
import urllib

host = '172.18.0.5'
database = 'speedtest'
mongo_username = ''
mongo_password = ''

with open('../data/secrets/speedtest-db_api_username', 'r') as user_secret:
    mongo_username = user_secret.read().strip()

with open('..//data/secrets/speedtest-db_api_password', 'r') as pass_secret:
    mongo_password = pass_secret.read().strip()

client = MongoClient('mongodb://%s:%s@%s/%s' % (mongo_username, mongo_password, host, database))

db = client.speedtest
collection = db.results

query_result = collection.find()
for doc in query_result:
    if isinstance(doc['fast'], float):
        continue
    elif 'Mbps' in doc['fast']:
        doc_id = doc['_id']
        
        try:
            for field in doc:
                if field in ['_id', 'client', 'timestamp']:
                    continue
                else:
                    speed = doc[field]
                    speed = float(speed.rstrip(' Mbps')) * 1000000
                    doc[field] = speed
        except:
            # remove entry
            print('Removing doc with id: %s' % str(doc_id))
            collection.delete_one({ "_id": ObjectId(doc_id)})
        
    else:
        continue
