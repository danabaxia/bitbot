from flask import render_template, flash, redirect, send_from_directory
from flask.helpers import url_for
from flask_login.utils import login_required
from flaskr import app
from flaskr.forms import *
from flask_login import current_user, login_user
from flaskr.models import User, Transaction, Balance, Test, Order
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from flaskr import db, mongo
from datetime import datetime
from flaskr.forms import EditProfileForm
import flaskr.data_source as bt 
from flaskr import socketio
from flask_socketio import SocketIO, send 
from flask import jsonify
import json
from pymongo import MongoClient
import threading, time 
##
import flaskr.data as dt

"""@app.before_first_request
def activate_job():
    def run_job():
        while True:
            print("Run recurring task")
            for order in Order.objects(status='filing'):
                print(order.method)
                if order.method == 'market':
                    if order.action == 'buy':
                        order.update(status='complete')
                        user = User.query.filter_by(username=order.user).first()
                        cash = user.balance[-1].cash_balance - order.amount
                        bitcoin_value = user.balance[-1].bitcoin_value + order.amount
                        bitcoin_amount = bitcoin_value/order.price
                        Balance(cash_balance=cash,bitcoin_amount=bitcoin_amount,bitcoin_value=bitcoin_value,user=user)
                        db.session.add(user)
                        db.session.commit()
                        print('market order buy complete')
                    elif order.action == 'sell':
                        order.update(status='complete')
                        user = User.query.filter_by(username=order.user).first()
                        cash = user.balance[-1].cash_balance + order.amount
                        bitcoin_value = user.balance[-1].bitcoin_value - order.amount
                        bitcoin_amount = bitcoin_value/order.price
                        Balance(cash_balance=cash,bitcoin_amount=bitcoin_amount,bitcoin_value=bitcoin_value,user=user)
                        db.session.add(user)
                        db.session.commit()
                        print('market order sell complete')
                elif order.method == 'limit':
                    if order.action == 'buy' and order.price >bt.get_cypto_price():
                        order.update(status='complete')
                        user = User.query.filter_by(username=order.user).first()
                        cash = user.balance[-1].cash_balance - order.amount
                        bitcoin_value = user.balance[-1].bitcoin_value + order.amount
                        bitcoin_amount = bitcoin_value/order.price
                        Balance(cash_balance=cash,bitcoin_amount=bitcoin_amount,bitcoin_value=bitcoin_value,user=user)
                        db.session.add(user)
                        db.session.commit()
                        print('limit order buy complete')
                    elif order.action == 'sell' and order.price <bt.get_cypto_price():
                        order.update(status='complete')
                        user = User.query.filter_by(username=order.user).first()
                        cash = user.balance[-1].cash_balance + order.amount
                        bitcoin_value = user.balance[-1].bitcoin_value - order.amount
                        bitcoin_amount = bitcoin_value/order.price
                        Balance(cash_balance=cash,bitcoin_amount=bitcoin_amount,bitcoin_value=bitcoin_value,user=user)
                        db.session.add(user)
                        db.session.commit()
                        print('limit order sell complete')



            time.sleep(3)
    thread = threading.Thread(target=run_job)
    thread.start()"""




@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/static/<path:path>')
def send_image(path):
    return send_from_directory('static', path)
 
@app.route('/')
@app.route('/index')
@login_required
def index():
    bt_price = bt.get_cypto_price()
    print('bt price', bt_price)

    return render_template('index.html', title='Home Page', bt_price=bt_price)


@socketio.on('message', namespace='/index')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('login'))
        r = login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        print('login_user',r)
        print('next page', next_page)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, phone=form.phone.data)
        user.set_password(form.password.data)
        balance = Balance(user=user)
        db.session.add(user)
        db.session.add(balance)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>', methods=['GET','POST'])
@login_required
def user(username):
    print('test')
    user = User.query.filter_by(username=username).first_or_404()
    print(user.balance[0].cash_balance)
    cash = user.balance[0].cash_balance
    bit = user.balance[0].bitcoin_value
    return render_template('summary.html',cash=cash,bit=bit)

@app.route('/user/<username>/summary', methods=['GET', 'POST'])
@login_required
def summary(username):
    #sample data of btc
    value_day = dt.value_day
    value_week = dt.value_week
    value_month = dt.value_month
    value_year = dt.data_as_dict_year
    value_all = dt.value_all
    hourly_value = dt.hourly_value

    # value_day = bt.request_CyptoPrice_hour(24)
    # value_week = bt.request_CyptoPrice_day(7)
    # value_month = bt.request_CyptoPrice_day(30)
    # value_year = bt.request_CyptoPrice_day(365)
    # value_all = bt.request_CyptoPrice_day()
    # hourly_value = bt.request_CyptoPrice_hour()
    #sample data of bit_value
    user = User.query.filter_by(username=username).first_or_404()
    balance= user.balance[-1]
    cash = user.balance[-1].cash_balance
    bit = user.balance[-1].bitcoin_value
    bit_amount = user.balance[-1].bitcoin_amount
    btc_now = bt.get_cypto_price()
    balance_dict = bt.get_balance_dict(username)
    print(balance_dict)
    change_d = round((btc_now - list(value_day.items())[-1][1])/list(value_day.items())[-1][1] * 100,2)
    change_m = round((btc_now - list(value_month.items())[-1][1])/list(value_month.items())[-1][1] * 100,2)
    change_y = round((btc_now - list(value_year.items())[-1][1])/list(value_year.items())[-1][1] * 100,2)
    change_all = round((btc_now - list(value_all.items())[-1][1])/list(value_all.items())[-1][1] * 100,2)
    if list(balance_dict.values())[-1] >0:
        change_balance = round(change_m*bit/list(balance_dict.values())[-1],2)
    else:
        change_balance = 0.0
    print(change_balance)

    return render_template('summary.html',balance=balance, balance_dict=balance_dict,change_balance=change_balance,
                           value_all=value_all, value_day=value_day, value_month=value_month, 
                           value_week=value_week, value_year=value_year, btc_now=btc_now,
                           change_d=change_d, change_m=change_m, change_y= change_y, change_all=change_all)

@app.route('/user/<username>/position')
@login_required
def position(username):
    user = User.query.filter_by(username=username).first_or_404()
    print(user.balance[0].cash_balance)
    balance= user.balance[0]
    cash = user.balance[0].cash_balance
    bit = user.balance[0].bitcoin_value
    return render_template('position.html',balance=balance)

@app.route('/user/<username>/market')
@login_required
def market(username):
    print('test')
    user = User.query.filter_by(username=username).first_or_404()
    print(type(user))
    return render_template('market.html')

@app.route('/user/<username>/trade', methods=['GET','POST'])
@login_required
def trade(username):
    form = TransactionForm()
    if request.method == "POST":
        user = User.query.filter_by(username=username).first()
        cash = user.balance[-1].cash_balance - form.amount.data
        bitcoin_value = user.balance[-1].bitcoin_value + form.amount.data
        bitcoin_amount = user.balance[-1].bitcoin_amount + form.amount.data/bt.get_cypto_price()
        Balance(cash_balance=cash,bitcoin_amount=bitcoin_amount,bitcoin_value=bitcoin_value,user=user)
        Transaction(amount=form.amount.data, action='Buy',
                                  order='Limit',price=form.price.data,status='Filing', user=user)
        db.session.add(user)
        db.session.commit() 
        balance = user.balance[-1]
        return render_template('trade.html', form=form)


    return render_template('trade.html', form=form)


@app.route('/user/<username>/analysis')
@login_required
def analysis(username):
    user = User.query.filter_by(username=username).first_or_404()
    balance = user.balance[-1]
    users = User.query.all()
    return render_template('analysis.html', balance=balance, users=users)

@app.route('/user/<username>/history', methods=['GET','POST'])
@login_required
def history(username):
    #data = user.transactions 
    data = Order.objects(user=username).order_by('-date')
    return render_template('history.html',data=data)

@app.route('/remove_order&ID=<string:order_id>', methods=['POST', 'GET'])
def remove_order(order_id):
    print ("Hello")
    print(order_id)
    Order(id=order_id).delete()
    return ('OK')

@app.route('/update_order&ID=<string:order_id>&price=<string:price_update>', methods=['POST', 'GET'])
def update_order(order_id, price_update):
    print(order_id)
    price = float(price_update)
    order = Order(id=order_id).update(price=price)
    print ("update complete")
    return ('OK')

#record user last visit 
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
 
#edit user profile
@app.route('/edit_profile', methods=['POST','GET'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/user/<username>/transfer', methods=["GET","POST"])
@login_required
def transfer(username):
    form = TransferForm()
    username = username
    if request.method == "POST":
        print('POST to transfer')
        print('cash', form.cash.data)
        user = User.query.filter_by(username=username).first()
        cash = user.balance[-1].cash_balance + form.cash.data
        bitcoin_value = user.balance[-1].bitcoin_value
        bitcoin_amount = user.balance[-1].bitcoin_amount
        Balance(cash_balance=cash,bitcoin_amount=bitcoin_amount,bitcoin_value=bitcoin_value,user=user)
        db.session.add(user)
        db.session.commit()
        balance = user.balance[-1]
        print(balance.cash_balance)
        return redirect(url_for('summary',username=username))
    return render_template('transfer.html', form=form)

@app.route('/api/get_btc_price', methods=["GET"])  
def get_current_price():
    return str(bt.get_cypto_price())

@app.route('/market_buy', methods=["POST","GET"])
def market_buy():
    form = OrderForm()
    if request.method == 'POST':
        form.user = current_user.username
        result = request.form
        form.action = 'buy'
        form.method = 'market'
        form.amount = float(result['amount'])
        form.price = bt.get_cypto_price()
        Order(user=form.user, action=form.action, amount=form.amount, price=form.price, method=form.method).save()
    return redirect(url_for('analysis',username=form.user))

@app.route('/market_buy_amount', methods=["POST","GET"])
def market_buy_amount():
    form = OrderForm()
    if request.method == 'POST':
        form.user = current_user.username
        result = request.form
        form.action = 'buy'
        form.method = 'market'
        form.price = bt.get_cypto_price()
        form.amount = float(result['amount'])*form.price
        Order(user=form.user, action=form.action, amount=form.amount, price=form.price, method=form.method).save()
    return redirect(url_for('analysis',username=form.user))

@app.route('/market_sell', methods=["POST","GET"])
def market_sell():
    form = OrderForm()
    if request.method == 'POST':
        form.user = current_user.username
        result = request.form
        form.action = 'sell'
        form.method = 'market'
        form.amount = float(result['amount'])
        form.price = bt.get_cypto_price()
        Order(user=form.user, action=form.action, amount=form.amount, price=form.price, method=form.method).save()
    return 'complete'

@app.route('/market_sell_amount', methods=["POST","GET"])
def market_sell_amount():
    form = OrderForm()
    if request.method == 'POST':
        form.user = current_user.username
        result = request.form
        form.action = 'sell'
        form.method = 'market'
        form.price = bt.get_cypto_price()
        form.amount = float(result['amount'])*form.price
        Order(user=form.user, action=form.action, amount=form.amount, price=form.price, method=form.method).save()
    return redirect(url_for('analysis',username=form.user))

@app.route('/limit_buy', methods=["POST","GET"])
def limit_buy():
    form = OrderForm()
    print('hi')
    if request.method == 'POST':
        form.user = current_user.username
        result = request.form
        form.action = 'buy'
        form.method = 'limit'
        form.amount = float(result['amount'])
        form.price = float(result['price'])
        Order(user=form.user, action=form.action, amount=form.amount, price=form.price, method=form.method).save()
        flash('Your changes have been saved.')
        print('sent order')
    return redirect(url_for('analysis',username=form.user))

@app.route('/limit_sell', methods=["POST","GET"])
def limit_sell():
    form = OrderForm()
    if request.method == 'POST':
        form.user = current_user.username
        result = request.form
        form.action = 'sell'
        form.method = 'limit'
        form.amount = float(result['amount'])
        form.price = float(result['price'])
        Order(user=form.user, action=form.action, amount=form.amount, price=form.price, method=form.method).save()
        flash('Your changes have been saved.')
    return redirect(url_for('analysis',username=form.user))

@app.route('/stop_buy', methods=["POST","GET"])
def stop_buy():
    form = OrderForm()
    if request.method == 'POST':
        form.user = current_user.username
        result = request.form
        form.action = 'buy'
        form.method = 'stop'
        form.amount = float(result['amount'])
        form.price = float(result['price'])
        Order(user=form.user, action=form.action, amount=form.amount, price=form.price, method=form.method).save()
        flash('Your changes have been saved.')
        print('sent order')
    return redirect(url_for('analysis',username=form.user))

@app.route('/stop_sell', methods=["POST","GET"])
def stop_sell():
    form = OrderForm()
    if request.method == 'POST':
        form.user = current_user.username
        result = request.form
        form.action = 'sell'
        form.method = 'stop'
        form.amount = float(result['amount'])
        form.price = float(result['price'])
        Order(user=form.user, action=form.action, amount=form.amount, price=form.price, method=form.method).save()
        flash('Your changes have been saved.')
        print('sent order')
    return redirect(url_for('analysis',username=form.user))

@app.route('/trail_buy', methods=["POST","GET"])
def trail_buy():
    form = OrderForm()
    if request.method == 'POST':
        form.user = current_user.username
        result = request.form
        form.action = 'buy'
        form.method = 'trail'
        form.amount = float(result['amount'])
        form.price = round((float(result['price'])/100 + 1)* bt.get_cypto_price(),2)
        Order(user=form.user, action=form.action, amount=form.amount, price=form.price, method=form.method).save()
        flash('Your changes have been saved.')
        print('sent order')
    return redirect(url_for('analysis',username=form.user))

@app.route('/trail_sell', methods=["POST","GET"])
def trail_sell():
    form = OrderForm()
    if request.method == 'POST':
        form.user = current_user.username
        result = request.form
        form.action = 'sell'
        form.method = 'trail'
        form.amount = float(result['amount'])
        form.price = round((1 - float(result['price'])/100)* bt.get_cypto_price(),2)
        Order(user=form.user, action=form.action, amount=form.amount, price=form.price, method=form.method).save()
        flash('Your changes have been saved.')
        print('sent order')
    return redirect(url_for('analysis',username=form.user))