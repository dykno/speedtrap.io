from app import app
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from flask import jsonify
from flask import request
from keylookup import KeyLookup
from mongodriver import MongoDriver

driver = MongoDriver()
client = driver.db_connection('speedtest-db', 'speedtest')
api_key_lookup = KeyLookup()

@app.route('/index')
def index():
    return "speedtrap.io web front end"

@app.route('/speedtest', methods=['GET'])
def get_speedtest():
    return "You've hit the speedtest page!"

@app.route('/speedtest/today', methods=['GET'])
def get_speedtest_today():
    db = client.speedtest
    collection = db.results
    
    now = datetime.now()
    today = now.strftime('%Y/%m/%d')

    query_result = collection.find({'timestamp':{'$lt': now.timestamp(), '$gt': (now - timedelta(hours=24)).timestamp()}})
    #query_result = collection.find({'timestamp':'test'})
    results = []
    for doc in query_result:
        print('%s - %s' % (type(doc), doc))
        [doc.pop(key) for key in ['client', '_id']]
        results.append(doc)
    
    return str(results)
