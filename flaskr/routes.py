from flask import render_template, flash, redirect, send_from_directory
from flask.helpers import url_for
from flask_login.utils import login_required
from flaskr import app
from flaskr.forms import LoginForm, RegistrationForm, TransferForm, TransactionForm
from flask_login import current_user, login_user
from flaskr.models import User, Transaction, Balance
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from flaskr import db
from datetime import datetime
from flaskr.forms import EditProfileForm
import flaskr.data_source as bt 
from flaskr import socketio
from flask_socketio import SocketIO, send 



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
        print('user',user.username)
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
    #bit_day = bt.request_CyptoPrice_day()['close']
    #print(bit_day)
    user = User.query.filter_by(username=username).first_or_404()
    balance= user.balance[-1]
    cash = user.balance[-1].cash_balance
    bit = user.balance[-1].bitcoin_value
    for b in user.balance:
        print('date', b.date)
    return render_template('summary.html',balance=balance)

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
        user.balance[0].cash_balance -= form.amount.data
        user.balance[0].bitcoin_value += form.amount.data
        db.session.commit() 
        print('amount',form.amount.data)
        print('price', form.price.data)
        transaction = Transaction(amount=form.amount.data, action='Buy',
                                  order='Limit',price=form.price.data,status='Filing', user=user)
        db.session.add(transaction)
        db.session.commit() 
        return render_template('summary.html', cash=user.balance[0].cash_balance, bit=user.balance[0].bitcoin_value)


    return render_template('trade.html', form=form)


@app.route('/user/<username>/analysis')
@login_required
def analysis(username):
    print('test')
    user = User.query.filter_by(username=username).first_or_404()
    print(type(user))
    return render_template('analysis.html')

@app.route('/user/<username>/history', methods=['GET','POST'])
@login_required
def history(username):
    user = User.query.filter_by(username=username).first_or_404()
    data = user.transactions 
    return render_template('history.html',data=data)

@app.route('/remove_order')
def background_process_test():
    print ("Hello")
    return ('nothing')

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

@app.route('/test', methods=["GET","POST"])
def test():
    if request.method == "POST":
        return 'this is post'
    return render_template('test.html')


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