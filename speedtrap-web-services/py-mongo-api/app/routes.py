from app import app
from bson.objectid import ObjectId
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
    db = client.speedtest
    collection = db.results
 
    try:   
        api_key = request.headers.get('auth')
        api_client = api_key_lookup.get_client_by_key(api_key)
        timestamp = request.json['timestamp']
        fast_result = request.json['fast']
        speedtest_result = request.json['speedtest']
        turnkey_result = request.json['turnkey']
        ookla_result = request.json['ookla']
    except:
        content = {'error': 'invalid data received'}
        return content, 500

    try:
        result_id = collection.insert({
            'client': api_client,
            'timestamp': timestamp,
            'fast': fast_result,
            'speedtest': speedtest_result,
            'turnkey': turnkey_result,
            'ookla': ookla_result
        })
    except Exception as e:
        content = {'error': 'insert failed'}
        return content, 500
    
    query_result = db.results.find_one({'_id':ObjectId(result_id)})
    content = {'success': str(query_result)}
    return content, 200

@app.route('/mongo_status')
def mongo_status():
    
    db = client.speedtest
    collections = db.collection_names()
    query_result = db.results.find()
    results = []
    for doc in query_result:
        results.append(doc)
    return "You've hit the status page! %s %s %s" % (collections, query_result, str(results))
    
