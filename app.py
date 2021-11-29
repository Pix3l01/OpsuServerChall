from flask import Flask, render_template, request
from pages.api import api
from bakand.db.dbClasses import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)
app.register_blueprint(api)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

