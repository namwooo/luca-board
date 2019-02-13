from marshmallow import post_load, fields, validate

from app import ma
from .models import Board


class BoardSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.Integer(dump_only=True)
    writer_id = fields.Integer()
    title = fields.String(validate=[
        validate.Length(min=1, max=240)
    ])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class BoardCreateSchema(ma.Schema):
    class Meta:
        strict = True

    title = fields.String(load_only=True, required=True, validate=[
        validate.Length(min=1, max=240)
    ])

    @post_load
    def make_board(self, data):
        return Board(**data)


class BoardUpdateSchema(ma.Schema):
    class Meta:
        strict = True

    title = fields.String(load_only=True, required=True, validate=[
        validate.Length(min=1, max=240)
    ])
