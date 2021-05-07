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



app = Flask(__name__, static_url_path='')
app.config.from_object(Config)
#config mongoDB
app.config['MONGODB_SETTINGS'] = {
    'db': 'app_mongo',
    'host': 'localhost',
    'port': 27017
}


db = SQLAlchemy(app)
db_nosql = MongoEngine()
db_nosql.init_app(app)

app.session_interface = MongoEngineSessionInterface(db_nosql)

migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

from flaskr import routes, models, errors


