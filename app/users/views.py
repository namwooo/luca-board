import base64
from urllib import response

from flask import request, make_response, redirect, session, jsonify
from flask_classful import FlaskView, route
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies
from flask_login import login_user, login_required, logout_user, encode_cookie

from app import db, lm, transaction, handle_error
from .models import User
from .schemas import UserSchema, LoginSchema, SignupSchema


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

        access_token = create_access_token(identity=user.id)
        resp = jsonify({'access_token': access_token})

        return resp, 200

    @route("/logout", methods=["GET"])
    # @login_required
    def logout(self):
        logout_user()

        return '', 200
