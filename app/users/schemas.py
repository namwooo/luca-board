from marshmallow import post_load, fields, validate, validates, ValidationError, validates_schema

from app import ma
from app.users.models import User


class UserSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(load_only=True, required=True, validate=[
        validate.Length(min=8, max=30)
    ])
    first_name = fields.String(required=True, validate=[
        validate.Length(min=2, max=35)
    ])
    last_name = fields.String(required=True, validate=[
        validate.Length(min=2, max=35)
    ])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('email')
    def check_email_duplication(self, email):
        user = User.query.filter(User.email == email).first()
        if user is not None:
            raise ValidationError('email is duplicated')

    @post_load
    def make_user(self, data):
        user = User(email=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    password=data['password'])
        return user


class LoginSchema(ma.Schema):
    class Meta:
        strict = True

    email = fields.Email(load_only=True, required=True)
    password = fields.String(load_only=True, required=True)

    @validates_schema()
    def validate_user(self, data):
        user = User.query.filter(User.email == data['email']).first()

        if user is None:
            raise ValidationError('user does not exist')

        if not user.password == data['password']:
            raise ValidationError('password does not match')

    @post_load
    def get_user(self, data):
        user = User.query.filter(User.email == data['email']).first()
        return user


user_schema = UserSchema()
users_schema = UserSchema(many=True)
