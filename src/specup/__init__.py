__version__ = '0.1.0'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI="mysql://luca@localhost/specup_db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=False
)

db = SQLAlchemy(app)

from specup import models

db.create_all()


# a simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'
