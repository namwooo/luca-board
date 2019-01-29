from marshmallow import post_load, fields, validate, validates, ValidationError, validates_schema

from app import ma
from app.users.models import User


class UserSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=[
        validate.Length(min=2, max=64)
    ])
    password1 = fields.String(load_only=True, required=True, validate=[
        validate.Length(min=8, max=30)
    ])
    password2 = fields.String(load_only=True, required=True, validate=[
        validate.Length(min=8, max=30)
    ])
    email = fields.Email(required=True)
    first_name = fields.String(required=True, validate=[
        validate.Length(min=2, max=35)
    ])
    last_name = fields.String(required=True, validate=[
        validate.Length(min=2, max=35)
    ])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates('username')
    def check_duplication_username(self, username):
        user = User.query.filter(User.username == username).first()
        if user is not None:
            raise ValidationError('username is duplicated')

    @validates('password1')
    def check_format_password1(self, password1):
        pass

    @validates_schema
    def confirm_passwords(self, data):
        if not data['password1'] == data['password2']:
            raise ValidationError('password1 and password2 must match')

    @post_load
    def make_user(self, data):
        user = User(username=data['username'],
                    email=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'])
        user.set_password(data['password1'])
        return user


class LoginSchema(ma.Schema):
    class Meta:
        strict = True

    username = fields.String(load_only=True, required=True)
    password = fields.String(load_only=True, required=True)

    @validates_schema()
    def check_password(self, data):
        user = User.query.filter(User.username == data['username']).first()
        if user is None:
            raise ValidationError('user does not exist')
        if not user.check_password(data['password']):
            raise ValidationError('password does not match')

    @post_load
    def get_user(self, data):
        user = User.query.filter(User.username == data['username']).first()
        return user


user_schema = UserSchema()
users_schema = UserSchema(many=True)
