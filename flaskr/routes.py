from flask import render_template, flash, redirect
from flask.helpers import url_for
from flask_login.utils import login_required
from flaskr import app
from flaskr.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user
from flaskr.models import User
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from flaskr import db
from datetime import datetime
from flaskr.forms import EditProfileForm
import flaskr.data_source as bt 
from flaskr import socketio
from flask_socketio import SocketIO, send 
 
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
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/user/<username>/summary')
@login_required
def summary(username):
    print('test')
    user = User.query.filter_by(username=username).first_or_404()
    print(type(user))
    return render_template('summary.html')

@app.route('/user/<username>/position')
@login_required
def position(username):
    print('test')
    user = User.query.filter_by(username=username).first_or_404()
    print(type(user))
    return render_template('position.html')

@app.route('/user/<username>/market')
@login_required
def market(username):
    print('test')
    user = User.query.filter_by(username=username).first_or_404()
    print(type(user))
    return render_template('market.html')

@app.route('/user/<username>/trade')
@login_required
def trade(username):
    print('test')
    user = User.query.filter_by(username=username).first_or_404()
    print(type(user))
    return render_template('trade.html')

@app.route('/user/<username>/analysis')
@login_required
def analysis(username):
    print('test')
    user = User.query.filter_by(username=username).first_or_404()
    print(type(user))
    return render_template('analysis.html')

@app.route('/user/<username>/history')
@login_required
def history(username):
    print('test')
    user = User.query.filter_by(username=username).first_or_404()
    print(type(user))
    return render_template('history.html')

#record user last visit 
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
 
#edit user profile
@app.route('/edit_profile', methods=['GET', 'POST'])
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


