import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:Jason2021@app.cruyrchd4npz.us-east-2.rds.amazonaws.com/app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #email
    ADMINS = ['danabaxia@gmail.com']
    