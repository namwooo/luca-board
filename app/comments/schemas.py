from marshmallow import fields, validate, post_load

from app import ma
from app.comments.models import Comment


class CommentsSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.Integer(dump_only=True)
    writer_id = fields.Integer(required=True)
    post_id = fields.Integer(required=True)
    comment_parent_id = fields.Integer()
    body = fields.String(required=True, validate=[
        validate.Length(min=1, max=65535)
    ])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_comment(self, data):
        comment = Comment(**data)

        return comment

