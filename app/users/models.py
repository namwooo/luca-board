from flask_login import UserMixin
from sqlalchemy_utils import EmailType, PasswordType

from app import db
from app.mixins import TimestampMixin


class User(db.Model, UserMixin, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)

    board = db.relationship('Board', backref='writer', lazy=True)
    post = db.relationship('Post', backref='writer', lazy=True)

    def __str__(self):
        return '{}'.format(self.email)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
