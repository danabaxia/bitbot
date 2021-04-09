from datetime import datetime
from flaskr import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flaskr import login
from hashlib import md5

class User(UserMixin, db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    mobilenumber = db.Column(db.String(128))
    address = db.Column(db.String(128))

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username
        
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


class Transaction(UserMixin, db.Model):
    __tablename__ = 'Transactions'

    transaction_id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(64), index=True)
    transaction_bitcoin_number = db.Column(db.Integer, index=True)
    bitcoin_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Transaction: {}>'.format(self.transaction_id)


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






