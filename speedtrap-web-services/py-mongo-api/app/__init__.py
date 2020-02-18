from flask import Flask
from keylookup import KeyLookup
from mongodriver import MongoDriver

app = Flask(__name__)

from app import routes
