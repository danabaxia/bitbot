from datetime import datetime
from flaskr import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flaskr import login_manager
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    address = db.Column(db.String(128))
    cash_balance = db.Column(db.Float, default=0)
    bitcoin_value = db.Column(db.Float, default=0)

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(16))
    order = db.Column(db.String(16))
    status = db.Column(db.String(16))
    amount = db.Column(db.Float)
    price = db.Column(db.Float)

class Product(UserMixin, db.Model):
    __tablename__ = 'Products'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    order = db.Column(db.String(16))
    subcription_type = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Product: {}>'.format(self.product_id)

class Strategy(UserMixin, db.Model):
    __tablename__ = 'Strategies'

    product_id = db.Column(db.Integer, primary_key=True)
    strategy_name = db.Column(db.String(64), index=True)
    product_strategy_algorithm = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Strategy: {}>'.format(self.product_id)
    
class BitPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exchange = db.Column(db.String())  
    price = db.Column(db.String())     
    horah = db.Column(db.DateTime)

    def __init__(self, exchange, price, horah):
        self.exchange = exchange
        self.price = price
        if horah is None:
            horah = datetime.utcnow()
        self.horah = horah

    def __repr__(self):
        return '<Exchange {}>'.format(self.exchange)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
