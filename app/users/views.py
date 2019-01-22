from flask import request, jsonify
from flask_classful import FlaskView, route
from werkzeug.routing import ValidationError
from werkzeug.security import generate_password_hash

from app import db
from app.users.models import User
from app.users.schema import user_schema


class UsersView(FlaskView):
    def index(self):
        all_users = User.all()
        result = user_schema.dump(all_users)
        return jsonify(result.data)

    def get(self, id):
        return 'model object'

    @route("/signup/", methods=["POST"])
    def post(self):
        data = request.get_json()

        if not data['password1'] == data['password2']:
            raise ValidationError('password1 and password2 must match')

        result = user_schema.load(data)
        new_user = result.data

        hashed_password = generate_password_hash(data['password1'])
        new_user.password = hashed_password

        db.session.add(new_user)
        db.session.commit()

        user = User.query.get(new_user.id)
        return user_schema.jsonify(user)
