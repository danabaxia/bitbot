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



app = Flask(__name__, static_url_path='')
app.config.from_object(Config)
#config mongoDB
client = pymongo.MongoClient("mongodb+srv://bobo1314:Hjb1314$@cluster0.c7xci.mongodb.net/app?retryWrites=true&w=majority")
mongo = client['app']

db = SQLAlchemy(app)
#db_nosql = MongoEngine()
#db_nosql.init_app(app)

migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

from flaskr import routes, models, errors


