from app import app
from pymongo import MongoClient
import urllib
import os
from app.mongodriver import MongoDriver

driver = MongoDriver()
client = driver.db_connection()

@app.route('/')
@app.route('/index')
def index():
    return "speedtrap.io API"

@app.route('/speedtest')
def speedtest():
    return "You've hit the speedtest page!"

@app.route('/mongo_status')
def mongo_status():
    
    '''
    with open(os.environ['MONGO_USERNAME'], 'r') as sec:
        mongo_username = sec.read().strip()

    with open(os.environ['MONGO_PASSWORD'], 'r') as sec:
        mongo_password = sec.read().strip()

    client = MongoClient('mongodb://%s:%s@speedtest-db/speedtest' % (mongo_username, mongo_password))
    '''
    db = client.speedtest
    collections = db.collection_names()
    query_result = db.results.find_one({'test-data': 'test-data'})
    return "You've hit the status page! %s %s" % (collections, query_result)
    
