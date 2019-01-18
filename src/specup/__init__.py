__version__ = '0.1.0'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:Demian!89@localhost/specup",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=False
)

db = SQLAlchemy(app)


# a simple page that says hello
@app.route('/')
def hello():
    return 'Hello, World!'
