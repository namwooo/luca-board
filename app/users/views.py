from flask import request, jsonify
from flask_classful import FlaskView, route
from flask_login import login_user, login_required, logout_user
from marshmallow import ValidationError

from app import db, lm
from .models import User
from .schemas import UserSchema, LoginSchema


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class UsersView(FlaskView):

    @route("/signup", methods=["POST"])
    def signup(self):
        data = request.get_json()
        user_schema = UserSchema()

        try:
            result = user_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), 422

        new_user = result.data

        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user), 201

    @route("/login", methods=["POST"])
    def login(self):
        data = request.get_json()

        login_schema = LoginSchema()
        user_schema = UserSchema()

        try:
            result = login_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), 422

        user = result.data
        login_user(user)

        return user_schema.jsonify(user), 200

    @route("/logout", methods=["GET"])
    @login_required
    def logout(self):
        logout_user()
        return '', 200
