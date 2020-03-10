from app import app
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from flask import jsonify
from flask import request
from flask import render_template
from keylookup import KeyLookup
from mongodriver import MongoDriver

driver = MongoDriver()
client = driver.db_connection('speedtest-db', 'speedtest')
api_key_lookup = KeyLookup()

@app.route('/')
def index():
    db = client.speedtest
    collection = db.results
    
    query_result = collection.find()
    results = []
    stats = {}
    stats['fast'] = {}
    stats['fast']['total'] = float(0)
    stats['fast']['count'] = float(0)
    for doc in query_result:
        [doc.pop(key) for key in ['client', '_id']]
        results.append(doc)
        if not isinstance(doc['fast'], float):
            stats['fast']['total'] += float(doc['fast'].rstrip(' Mbps'))
        else:
            stats['fast']['total'] += doc['fast']
        stats['fast']['count'] += 1

    stats['fast']['avg'] = stats['fast']['total'] / stats['fast']['count']
    print(stats)

    return render_template('index.html', data = results, stats = stats)

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
