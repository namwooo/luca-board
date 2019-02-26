from marshmallow import fields, validate, post_load, validates, ValidationError

from app import ma
from app.comments.models import Comment
from app.posts.models import Post


class CommentSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.Integer(dump_only=True)
    writer_id = fields.Integer(required=True)
    post_id = fields.Integer(required=True)
    comment_parent_id = fields.Integer()
    body = fields.String(required=True, validate=[
        validate.Length(min=1, max=20000)
    ])
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_comment(self, data):
        comment = Comment(**data)

        return comment


class CommentWriteSchema(ma.Schema):
    class Meta:
        strict = True

    body = fields.String(required=True, validate=[
        validate.Length(min=1, max=20000)
    ])

    @post_load
    def make_comment(self, data):
        return Comment(**data, writer=self.context['writer'])


class CommentsUpdateSchema(ma.Schema):
    class Meta:
        strict = True

    body = fields.String(required=True, validate=[
        validate.Length(min=1, max=65535)
    ])

    @post_load
    def update_comment(self, data):
        comment = self.context['instance']
        comment.body = data['body']

        return comment
