from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from flask import send_from_directory
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
import threading, time, requests




app = Flask(__name__, static_url_path='')
app.config.from_object(Config)
#config mongoDB
#client = pymongo.MongoClient("mongodb+srv://test:test@cluster0.c7xci.mongodb.net/app?retryWrites=true&w=majority")
#mongo = client['app']
DB_URI = "mongodb+srv://test:test@cluster0.c7xci.mongodb.net/app?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

mongo = MongoEngine(app)

db = SQLAlchemy(app)
mongo = MongoEngine()
mongo.init_app(app)

migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

from flaskr import routes, models, errors


