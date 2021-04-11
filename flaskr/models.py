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
    cash_balance = db.Column(db.Float)
    bitcoin_value = db.Column(db.Float)

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
    date = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.column(db.String(16))
    order = db.column(db.String(16))
    status = db.column(db.String(16))
    amount = db.column(db.Float)
    price = db.column(db.Float)
    user_id = db.column(db.Integer, db.ForeignKey('user.id'))

class Product(UserMixin, db.Model):
    __tablename__ = 'Products'

    product_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
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

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))