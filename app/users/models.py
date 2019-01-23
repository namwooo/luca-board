from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from sqlalchemy import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False,
                           server_default=func.now(),
                           server_onupdate=func.now())
    board = db.relationship('Board', backref='writer', lazy=True)

    def __str__(self):
        return '{}'.format(self.username)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
