from flask_classful import FlaskView, route
from werkzeug.exceptions import abort

from app import db
from app.posts.schemas import posts_list_schema, posts_detail_schema
from .models import Post


class PostsView(FlaskView):

    @route("/", methods=['GET'])
    def list(self):
        """List all posts ordered by created date"""
        posts = Post.query.filter_by(is_published=True).order_by(Post.created_at)

        if posts is None:
            abort(404)

        return posts_list_schema.jsonify(posts), 200

    @route("/<id>/", methods=['GET'])
    def detail(self, id):
        """Detail a post and plus view count"""
        post = Post.query.filter_by(id=id, is_published=True).first_or_404()

        post.view_count += 1

        db.session.add(post)
        db.session.commit()

        return posts_detail_schema.jsonify(post), 200

    @route("/rank/", methods=['GET'])
    def rank(self):
        """List ranked posts by its like counts"""
        posts = Post.query.filter_by(is_published=True)\
            .order_by(Post.like_count.desc()).limit(10)

        if posts is None:
            abort(404)

        return posts_list_schema.jsonify(posts), 200
