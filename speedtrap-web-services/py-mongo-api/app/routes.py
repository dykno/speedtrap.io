from app import app
from flask import jsonify
from flask import request
from keylookup import KeyLookup
from mongodriver import MongoDriver

driver = MongoDriver()
client = driver.db_connection()
api_key_lookup = KeyLookup()

@app.route('/index')
def index():
    return "speedtrap.io API"

@app.route('/speedtest', methods=['GET'])
def get_speedtest():
    return "You've hit the speedtest page!"

@app.route('/speedtest', methods=['POST'])
def add_speedtest():
    global client
    db = client.speedtest
    collection = db.results
    
    api_key = request.headers.get('auth')
    client = api_key_lookup.get_client_by_key(api_key)
    timestamp = request.json['timestamp']
    fast_result = request.json['fast']
    speedtest_result = request.json['speedtest']
    turnkey_result = request.json['turnkey']
    ookla_result = request.json['ookla']

    try:
        result_id = collection.insert({
            'client': client,
            'timestamp': timestamp,
            'fast': fast_result,
            'speedtest': speedtest_result,
            'turnkey': turnkey_result,
            'ookla': ookla_result
        })
    except Exception as e:
        print(e)

    cursor = list(collection.find({}))
    print(cursor)
    result = []
    for doc in cursor:
        result.append(doc)

    return str(result)

@app.route('/mongo_status')
def mongo_status():
    
    db = client.speedtest
    collections = db.collection_names()
    query_result = db.results.find_one({'test-data': 'test-data'})
    return "You've hit the status page! %s %s" % (collections, query_result)
    
