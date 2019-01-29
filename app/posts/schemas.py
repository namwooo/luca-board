from app import ma


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


posts_list_schema = PostsListSchema(many=True)
posts_detail_schema = PostsDetailSchema()
