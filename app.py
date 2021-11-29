from flask import Flask, render_template, request, redirect
from api import api
from auth import auth
from bakand.db.dbClasses import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BananaGelatosaViennente'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
app.register_blueprint(api)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

