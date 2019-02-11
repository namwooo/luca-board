from flask_login import UserMixin
from sqlalchemy_utils import EmailType, PasswordType

from app import db
from app.mixins import TimestampMixin


class User(db.Model, UserMixin, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha256']), nullable=False)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)

    boards = db.relationship('Board', back_populates='writer', lazy='select')
    posts = db.relationship('Post', back_populates='writer', lazy='select')
    comments = db.relationship('Comment', back_populates='writer', lazy='select')

    def __repr__(self):
        return '<{}(id: {}, name: {}, email: {}, is_admin: {}, is_active: {})>'\
            .format(self.__class__.__name__, self.id, self.full_name, self.email,
                    self.is_admin, self.is_active)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
