from datetime import datetime
from flaskr import db, db_nosql
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

    transactions = db.relationship('Transaction', backref=db.backref('user',lazy=True))
    products = db.relationship('Product', backref=db.backref('user',lazy=True))

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

class Balance(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    cash_balance = db.Column(db.Float, default=0)
    bitcoin_value = db.Column(db.Float, default=0)
    bitcoin_amount = db.Column(db.Float, default=0)
    hedge = db.Column(db.Float, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('balance',lazy=True))

    def __repr__(self):
        return '<Balance: {}>'.format(self.id)

"""
order: market,limit,stop,recurring, hedge 
action: buy, sell
status: filling, complete
"""
class Transaction(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(16))
    order = db.Column(db.String(16))
    status = db.Column(db.String(16))
    amount = db.Column(db.Float)
    price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

    def __repr__(self):
        return '<Transaction: {}>'.format(self.id)


class Product(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.String(16))
    subscription_type = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    strategies = db.relationship('Strategy', backref=db.backref('product',lazy=True))

    def __repr__(self):
        return '<Product: {}>'.format(self.id)


class Strategy(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strategy_name = db.Column(db.String(64), index=True)
    product_strategy_algorithm = db.Column(db.String(64), index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
  
    def __repr__(self):
        return '<Strategy: {}>'.format(self.strategy_name)
    

class BitPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    symbol = db.Column(db.String(64), default='BTC')
    price = db.Column(db.Float)     
    horah = db.Column(db.DateTime)

    def __init__(self, price, horah):
        self.price = price
        if horah is None:
            horah = datetime.utcnow()
        self.horah = horah
    def __repr__(self):
        return '<Symbol: {}>'.format(self.symbol)

##############
#Nosql db
"""
maket order
{
    "_id": 111,
    "user": "admin",
    "date":       ,
    "type": 
    "amount":      ,
    "price":
    "status":
}

limit order 
{
    "_id": ,
    "user":,
    "date":,
    "type":,
    "amount":,
    "limit_price":,
    "status":
}

stop order
{
    "_id":,
    "user":,
    "date":,
    "type":,
    "amount":,
    "stop_price":,
    "status":
}
"""
class Order_market(db_nosql.Document):
    id = db_nosql.IntField()
    name = db_nosql.StringField()

    def to_json(self):
        return { "id": self.id, 
                 "name": self.name}




@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


