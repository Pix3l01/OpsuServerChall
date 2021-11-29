from flask import Blueprint, request, redirect, render_template
from bakand.db.dbClasses import db, User

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            user = request.form['user']
            password = request.form['password']
            db.session.add(User(username=user, accountPassword=password))
            db.session.commit()
        except Exception as e:
            # TODO: handle exceptions
            print(e)
        return redirect('/register')
    return render_template('register.html')


@auth.route('/login')
def login():
    return 'login'


@auth.route('/logout')
def logout():
    return 'logout'
