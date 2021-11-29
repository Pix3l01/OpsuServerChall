from flask import Flask, render_template, request, redirect
from flask_login import LoginManager
from api import api
from auth import auth
from profile import profile
from bakand.db.dbClasses import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BananaGelatosaViennente'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


app.register_blueprint(api)
app.register_blueprint(auth)
app.register_blueprint(profile)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

