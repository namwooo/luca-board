from flask import request, jsonify
from flask_classful import FlaskView, route

from app.users.models import User
from app.users.schema import UserSchema


class UserView(FlaskView):
    def users(self):
        all_users = User.all()
        result = UserSchema.dump(all_users)
        return jsonify(result.data)

    @route('/signin', endpoint='signin')
    def post(self):
        data = request.data
        UserSchema.jsonify(data)
