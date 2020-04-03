from app import app
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from flask import jsonify
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from flask import url_for
from functools import wraps
import json
from os import environ as env
from six.moves.urllib.parse import urlencode
from werkzeug.exceptions import HTTPException

# Load Auth0 config values
with open(env['AUTH0_CONFIG'], 'r') as file_in:
    auth0_config = json.load(file_in)

print(auth0_config)
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=auth0_config['client_id'],
    client_secret=auth0_config['client_secret'],
    api_base_url=auth0_config['api_base_url'],
    access_token_url=auth0_config['access_token_url'],
    authorize_url=auth0_config['authorize_url'],
    client_kwargs={
        'scope': auth0_config['scope']
    },
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect('https://speedtrap.io')
        return f(*args, **kwargs)

    return decorated

# Handle Auth0 Callback
@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    return redirect('https://speedtrap.io/')

# Handle Login Auth0
@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='https://speedtrap.io/callback')

@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': 'https://speedtrap.io/', 'client_id': auth0_config['client_id']}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
            userinfo=session['profile'],
            userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))
