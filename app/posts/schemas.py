from marshmallow import post_load

from app import ma
from app.posts.models import Post


class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'writer_id', 'board_id',
                  'title', 'body', 'is_published',
                  'created_at', 'updated_at')

    @post_load
    def make_board(self, data):
        return Post(**data)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
