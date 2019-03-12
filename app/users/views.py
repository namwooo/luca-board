from flask import request, jsonify
from flask_classful import FlaskView, route
from flask_jwt_extended import create_access_token

from app import db, transaction, handle_error
from .schemas import UserSchema, LoginSchema, SignupSchema


class UserView(FlaskView):
    decorators = [transaction, handle_error]

    @route("/signup", methods=["POST"])
    def signup(self):
        data = request.data

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
