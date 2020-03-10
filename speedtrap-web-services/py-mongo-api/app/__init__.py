from flask import Flask
import os
import sys

route_config = os.environ['ROUTE_CONFIG'].strip()

if route_config == 'api':
    app = Flask(__name__)
    from app.api import routes
elif route_config == 'web':
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'web', 'templates'), static_folder=os.path.join(os.path.dirname(__file__), 'web', 'static'))
    from app.web import routes
else:
    print('ERROR: No route_config found. Exiting.')
    sys.exit()
