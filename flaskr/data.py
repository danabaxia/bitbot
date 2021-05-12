import requests 
import pandas as pd 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
import time
import datetime


app = Flask(__name__)
mysql = MySQL()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:QianWei@910712@localhost/app'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'QianWei@910712'
app.config['MYSQL_DATABASE_DB'] = 'app'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


conn = mysql.connect()
cursor =conn.cursor()

cursor.execute("SELECT * from BitPrice")
data = cursor.fetchall()

#### hourly_value
data_as_dict_hour = dict((str(y), x) for x, y in data if y.strftime("%M:%S") == '00:00')
#print(data_as_dict_hour)
hourly_value = data_as_dict_hour

#### value_day
data_as_dict_days = dict((str(y), x) for x, y in data if y.strftime("%X") == '00:00:00')
#print(data_as_dict_days)
data_as_dict_day = dict(list(data_as_dict_hour.items())[:24])
#print(data_as_dict_day)
value_day = data_as_dict_day

#### value_week 
data_as_dict_week = dict(list(data_as_dict_days.items())[:7])
#print(data_as_dict_week)
value_week = data_as_dict_week

#### value_month
data_as_dict_month = dict(list(data_as_dict_days.items())[:30])
#print(data_as_dict_month)
value_month = data_as_dict_month

#### value_year
data_as_dict_year = dict(list(data_as_dict_days.items())[:365])
#print(data_as_dict_year)
value_year = data_as_dict_year

#### value_all
data_as_dict_all = dict(list(data_as_dict_days.items()))
#print(data_as_dict_all)
value_all = data_as_dict_all