from flask import Blueprint, request, redirect, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

from bakand.db.dbClasses import db, User
from bakand.cryptography import createGuid

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form.get('user')
            password = request.form.get('password')
            print(username, password)
            user = User.query.filter_by(username=username).first()
            print(user)
            if user:
                flash('User already exists')
                return redirect('/register')
            db.session.add(User(username=username, password=generate_password_hash(password, method='sha256'), guid=createGuid()))
            db.session.commit()
        except Exception as e:
            # TODO: handle exceptions
            print(e)
        return redirect('/login')
    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # login code goes here
        username = request.form.get('user')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect('/login')  # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect('/profile')
    return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')
