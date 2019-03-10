from marshmallow import fields, validate, post_load

from .. import ma
from ..posts.models import Post


class WriterSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True, attribute='full_name')


class BoardSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.Integer(dump_only=True)
    title = fields.String(dump_only=True)


class PostSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.Integer(dump_only=True)
    board = fields.Nested(BoardSchema)
    writer = fields.Nested(WriterSchema)
    title = fields.String(required=True, validate=[
        validate.Length(min=1, max=120)
    ])
    is_published = fields.Boolean(required=True)
    has_image = fields.Boolean(required=True)
    like_count = fields.Integer(dump_only=True)
    view_count = fields.Integer(dump_only=True)
    comment_count = fields.Method('get_comment_count')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def get_comment_count(self, obj):
        return obj.comment_count


class PostWriteSchema(ma.Schema):
    class Meta:
        strict = True

    writer_id = fields.Integer(required=True)
    board_id = fields.Integer(required=True)
    has_image = fields.Boolean(required=True)
    title = fields.String(required=True, validate=[
        validate.Length(min=1, max=120)
    ])
    body = fields.String(required=True, validate=[
        validate.Length(min=1, max=20000)
    ])
    is_published = fields.Boolean(required=True)

    @post_load
    def make_post(self, data):
        return Post(**data)


class PostDetailSchema(PostSchema):
    class Meta:
        strict = True

    next_post = fields.Nested(PostSchema)
    prev_post = fields.Nested(PostSchema)
    is_user_like = fields.Boolean(required=True)
    body = fields.String(required=True, validate=[
        validate.Length(min=1, max=20000)
    ])


class PostUpdateSchema(ma.Schema):
    title = fields.String(required=True, validate=[
        validate.Length(min=1, max=120)
    ])
    body = fields.String(required=True, validate=[
        validate.Length(min=1, max=20000)
    ])
    is_published = fields.Boolean(required=True)


class PagedPostSchema(ma.Schema):
    total = fields.Integer()
    per_page = fields.Integer()
    page = fields.Integer()
    items = fields.Nested(PostSchema, many=True)


class PostsListSchema(ma.Schema):
    class Meta:
        fields = ('id', 'writer_id', 'board_id',
                  'title', 'like_count', 'view_count',
                  'is_published', 'created_at', 'updated_at',)


class PostsDetailSchema(ma.Schema):
    class Meta:
        fields = ('id', 'writer_id', 'board_id',
                  'title', 'body', 'like_count', 'view_count',
                  'is_published', 'created_at', 'updated_at',)


class PostsSchema(ma.Schema):
    class Meta:
        strict = True

    id = fields.Integer(dump_only=True)
    writer_id = fields.Integer(required=True)
    board_id = fields.Integer(required=True)
    writer = fields.String(dump_only=True)  # nested schema
    title = fields.String(required=True, validate=[
        validate.Length(min=1, max=120)
    ])
    body = fields.String(required=True, validate=[
        validate.Length(min=1, max=20000)
    ])
    is_published = fields.Boolean(required=True)
    like_count = fields.Integer(dump_only=True)
    view_count = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_post(self, data):
        post = Post(**data)

        return post


class PostsUpdateSchema(PostsSchema):
    @post_load
    def update_post(self, data):
        post = self.context['instance']
        post.title = data['title']
        post.body = data['body']
        post.is_published = data['is_published']

        return post
