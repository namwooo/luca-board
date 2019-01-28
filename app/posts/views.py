from flask_classful import FlaskView, route

from app.posts.schemas import posts_schema
from .models import Post


class PostsView(FlaskView):

    @route("/", methods=['GET'])
    def list(self):
        """List all posts ordered by created date"""
        posts = Post.query.order_by(Post.created_at).all()

        return posts_schema.jsonify(posts), 200
