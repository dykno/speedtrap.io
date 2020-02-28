from flask import Flask
import os
import sys

app = Flask(__name__)

route_config = os.environ['ROUTE_CONFIG'].strip()

if route_config == 'api':
    from app.api import routes
elif route_config == 'web':
    from app.web import routes
else:
    print('ERROR: No route_config found. Exiting.')
    sys.exit()
