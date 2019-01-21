from app import ma
from app.users.models import User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
