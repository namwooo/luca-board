from flask import request
from flask_classful import FlaskView, route
from flask_login import login_user, login_required, logout_user
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized

from app import db, lm
from .models import User
from .schema import user_schema


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class UsersView(FlaskView):

    @route("/signup/", methods=["POST"])
    def signup(self):
        data = request.get_json()
        if not data['password1'] == data['password2']:
            raise BadRequest('password1 and password2 must match')

        result = user_schema.load(data)
        new_user = result.data

        new_user.set_password(data['password1'])

        db.session.add(new_user)
        db.session.commit()

        user = User.query.get(new_user.id)
        return user_schema.jsonify(user)

    @route("/login/", methods=["POST"])
    def login(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user is None:
            raise NotFound

        if not user.check_password(password):
            raise Unauthorized

        login_user(user)

        return user_schema.jsonify(user)

    @login_required
    def logout(self):
        logout_user()
        return 'Logout success'
