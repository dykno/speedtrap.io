from app import app

@app.route('/')
@app.route('/index')
def index():
    return "speedtrap.io API"

@app.route('/speedtest')
def speedtest():
    return "You've hit the speedtest page!"
    
