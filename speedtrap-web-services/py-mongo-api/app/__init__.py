from flask import Flask
import os
from os import environ as env
import sys

# Determine which set of routes and configurations that we are dealing with.
route_config = env['ROUTE_CONFIG'].strip()

# If we're dealing with an API route configuration, load our basic API routes.
if route_config == 'api':
    app = Flask(__name__)
    from app.api import routes

# IF we're dealing with the web app configuration, load web routes and dependencies.
elif route_config == 'web':

    with open(env['APP_SECRET'], 'r') as secret:
        app_secret = secret.read().strip()

    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'web', 'templates'), static_folder=os.path.join(os.path.dirname(__file__), 'web', 'static'))

    app.secret_key = app_secret
    
    from app.web import routes
    from app.web import auth_routes

else:
    print('ERROR: No route_config found. Exiting.')
    sys.exit()
