from flask import request
from flask_classful import FlaskView, route
from flask_login import current_user, login_required
from sqlalchemy import and_

from .. import db, handle_error, transaction
from ..boards.models import Board
from ..posts.schemas import PostWriteSchema, \
    PagedPostSchema, PostDetailSchema, PostSchema, PostUpdateSchema
from .models import Post


class PostView(FlaskView):
    decorators = [transaction, handle_error]

    @route("boards/<board_id>/posts", methods=['GET'])
    def list(self, board_id):
        """List all published posts in board ordered by created date"""
        page = request.args.get('p', default=1, type=int)
        board = Board.query.get_or_404(board_id)

        posts = Post.query.filter(Post.board_id == board_id) \
            .filter(Post.is_published == True) \
            .order_by(Post.created_at.desc()) \
            .paginate(page=page, per_page=15, error_out=False)

        paged_post_schema = PagedPostSchema(context=posts)

        return paged_post_schema.jsonify(posts), 200

    @route('/posts', methods=['POST'])
    @login_required
    def post(self):
        """Create a post in board"""
        json_data = request.get_json()
        board = Board.query.get_or_404(json_data['board_id'])

        post_write_schema = PostWriteSchema(context={'writer': current_user})
        post = post_write_schema.load(json_data)
        post = post.data

        board.add_post(post)

        return '', 201

    @route('/posts/<id>', methods=['GET'])
    def get(self, id):
        """Detail a post and plus view count"""
        post = Post.query.filter(and_(Post.id == id, Post.is_published == True)).first_or_404()

        post.read()

        post_detail_schema = PostDetailSchema()
        return post_detail_schema.jsonify(post), 200

    @route('/posts/<id>', methods=['PATCH'])
    @login_required
    def patch(self, id):
        """Update a post"""
        json_data = request.get_json()
        post = Post.query.get_or_404(id)

        post_update_schema = PostUpdateSchema()
        post_update_schema.load(json_data)

        post.title = json_data['title']
        post.body = json_data['body']
        post.is_published = json_data['is_published']

        return '', 200

    @route('/posts/<id>', methods=['DELETE'])
    @login_required
    def delete(self, id):
        """Delete a post"""
        post = Post.query.get_or_404(id)

        db.session.delete(post)

        return '', 200

    @route('/posts/rank', methods=['GET'])
    def rank(self):
        """List ranked posts by its like counts"""
        posts = Post.query.filter(Post.is_published == True) \
            .order_by(Post.like_count.desc()) \
            .limit(10).all()

        posts_schema = PostSchema(many=True)
        return posts_schema.jsonify(posts), 200

    @route('/posts/<id>/like', methods=['PATCH'])
    @login_required
    def like(self, id):
        """Plus 1 like count for the post"""
        post = Post.query.get_or_404(id)

        post.like()

        return '', 200

    @route('/posts/<id>/unlike', methods=['PATCH'])
    @login_required
    def unlike(self, id):
        """Minus 1 like count for the post"""
        post = Post.query.get_or_404(id)

        post.unlike()

        return '', 200
