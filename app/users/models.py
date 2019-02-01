from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import EmailType, PasswordType

from app import db

from app.mixins import TimestampMixin


class User(db.Model, UserMixin, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(PasswordType, nullable=False)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)

    board = db.relationship('Board', backref='writer', lazy=True)
    post = db.relationship('Post', backref='writer', lazy=True)

    @hybrid_property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return '{}'.format(self.email)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @classmethod
    def create_user(self, email, password, first_name, last_name, is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name or last_name:
            raise ValueError("User must have first_name and last_name")

        user = self.model(
            email='',
            first_name=first_name,
            last_name=last_name,
            is_active=is_active
        )

        user.password = password

        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def create_superuser(self, email, password, first_name, last_name, is_active=True):
        user = self.create_user(email=email, password=password, first_name=first_name,
                                last_name=last_name, is_active=is_active)
        user.is_admin = True

        db.session.add(user)
        db.session.commit()

        return user
