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
    
    # Loop through all results in the database
    for doc in query_result:
        
        # Drop sensitive / unneeded fields
        [doc.pop(key) for key in ['client', '_id']]

        # Add to a list to generate table of all results
        results.append(doc)

        # Analyze each result to generate metrics        
        for key in doc:
            
            # Disregard timestamp field
            if key == 'timestamp':
                continue
            else:
                # Make sure we have our dictionary setup correctly
                if key not in stats:
                    stats[key] = {}
                    stats[key]['total'] = float(0)
                    stats[key]['count'] = float(0)
                
                # Check if we're dealing with a field that is in an old format
                # Tally up the result of each speedtest to calculate average
                if not isinstance(doc[key], float):
                    stats[key]['total'] += float(doc[key].rstrip(' Mbps'))
                else:
                    stats[key]['total'] += doc[key]

            # Increment counter to calculate average
            stats[key]['count'] += 1

            # Calculate average and add it to the result's dictionary
            stats[key]['avg'] = stats[key]['total'] / stats[key]['count']
    
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
