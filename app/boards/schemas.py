from marshmallow import post_load, fields, validate, pre_load

from app import ma
from .models import Board


class BoardsSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.Integer(dump_only=True)
    writer_id = fields.Integer(required=True)
    title = fields.String(required=True, validate=[
        validate.Length(min=1, max=240)
    ])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_board(self, data):
        return Board(**data)


board_schema = BoardsSchema()
boards_schema = BoardsSchema(many=True)
