import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Hjb1314$@localhost/app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #email
    ADMINS = ['danabaxia@gmail.com']
