from marshmallow import post_load

from app import ma
from app.users.models import User


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username',
                  'email', 'first_name',
                  'last_name', 'is_admin',
                  'created_at', 'updated_at')

    @post_load
    def make_user(self, data):
        return User(**data)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
