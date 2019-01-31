from marshmallow import fields, validate, post_load

from app import ma
from app.posts.models import Post


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
    writer_id = fields.Integer(dump_only=True, required=True)
    board_id = fields.Integer(dump_only=True, required=True)
    title = fields.String(required=True, validate=[
        validate.Length(min=1, max=120)
    ])
    body = fields.String(required=True, validate=[
        validate.Length(min=1)
    ])
    is_published = fields.Boolean(required=True)
    like_count = fields.Integer(dump_only=True)
    view_count = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def make_post(self, data):
        post = Post(writer_id=self.context['writer_id'],
                    board_id=self.context['board_id'],
                    title=data['title'],
                    body=data['body'],
                    is_published=data['is_published'])
        return post


class PostsUpdateSchema(PostsSchema):
    @post_load
    def make_post(self, data):
        post = self.context['instance']
        post.title = data['title']
        post.body = data['body']
        post.is_published = data['is_published']

        return post


posts_list_schema = PostsListSchema(many=True)
posts_detail_schema = PostsDetailSchema()
