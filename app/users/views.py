from flask import request, abort
from flask_classful import FlaskView, route
from flask_login import login_user, login_required, logout_user

from app import db, lm
from app.exceptions import PasswordDoesNotMatch, UserDoesNotExist
from .models import User
from .schemas import user_schema


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class UsersView(FlaskView):

    @route("/signup/", methods=["POST"])
    def signup(self):
        data = request.get_json()
        if not data['password1'] == data['password2']:
            raise PasswordDoesNotMatch('password1 and password2 must match')

        result = user_schema.load(data)
        new_user = result.data

        new_user.set_password(data['password1'])

        db.session.add(new_user)
        db.session.commit()

        user = User.query.get(new_user.id)
        return user_schema.jsonify(user), 201

    @route("/login/", methods=["POST"])
    def login(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if user is None:
            raise UserDoesNotExist('User does not exist')

        if not user.check_password(password):
            raise PasswordDoesNotMatch('password does not match')

        login_user(user)

        return user_schema.jsonify(user), 200

    @login_required
    def logout(self):
        logout_user()
        return 'Logout success', 200
