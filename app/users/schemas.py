from marshmallow import post_load, fields, validate, validates, ValidationError, validates_schema

from app import ma
from app.users.models import User


class UserSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.Integer(dump_only=True)
    email = fields.Email()
    password = fields.String(load_only=True)
    first_name = fields.String()
    last_name = fields.String()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class SignupSchema(ma.Schema):
    class Meta:
        strict = True

    email = fields.Email(required=True)
    # Password needs validation for combination
    password = fields.String(required=True, validate=[
        validate.Length(min=8, max=35)
    ])
    first_name = fields.String(required=True, validate=[
        validate.Length(min=1, max=35)
    ])
    last_name = fields.String(required=True, validate=[
        validate.Length(min=1, max=35)
    ])

    @validates('email')
    def check_email_duplication(self, email):
        user = User.query.filter(User.email == email).first()
        if user is not None:
            raise ValidationError('email is duplicated')

    @post_load
    def make_user(self, data):
        return User(**data)


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
