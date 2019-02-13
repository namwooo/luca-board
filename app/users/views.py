from flask import request
from flask_classful import FlaskView, route
from flask_login import login_user, login_required, logout_user

from app import db, lm, transaction, handle_error
from .models import User
from .schemas import UserSchema, LoginSchema, SignupSchema


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class UserView(FlaskView):
    decorators = [transaction, handle_error]

    @route("/signup", methods=["POST"])
    def signup(self):
        data = request.get_json()

        signup_schema = SignupSchema()
        new_user = signup_schema.load(data).data

        db.session.add(new_user)
        db.session.flush()

        user_schema = UserSchema()
        return user_schema.jsonify(new_user), 201

    @route("/login", methods=["POST"])
    def login(self):
        data = request.get_json()

        login_schema = LoginSchema()
        user = login_schema.load(data).data

        login_user(user)

        return '', 200

    @route("/logout", methods=["GET"])
    @login_required
    def logout(self):
        logout_user()

        return '', 200
