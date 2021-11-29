from flask import Blueprint, request, redirect, render_template, flash
from bakand.db.dbClasses import db, User

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
            db.session.add(User(username=username, accountPassword=password))
            db.session.commit()
        except Exception as e:
            # TODO: handle exceptions
            print(e)
        return redirect('/login')
    return render_template('register.html')


@auth.route('/login')
def login():
    return 'login'


@auth.route('/logout')
def logout():
    return 'logout'
