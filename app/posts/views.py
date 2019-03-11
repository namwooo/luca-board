from flask import request
from flask_classful import FlaskView, route
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_, desc

from app.helpers import convert_dump
from app.users.models import User
from .. import db, transaction, handle_error
from ..boards.models import Board
from ..posts.schemas import (
    PostWriteSchema,
    PagedPostSchema,
    PostDetailSchema,
    PostSchema,
    PostUpdateSchema
)
from .models import Post


class PostView(FlaskView):
    decorators = [transaction, handle_error]

    @route("/boards/<board_id>/posts", methods=['GET'])
    def list(self, board_id):
        """List all published posts in board ordered by created date"""
        page = int(request.args.get('page', 1))
        board = Board.query.get_or_404(board_id)

        posts = Post.query.filter(Post.board_id == board_id) \
            .filter(Post.is_published == True) \
            .order_by(Post.created_at.desc()) \
            .paginate(page=page, per_page=15, error_out=False)

        paged_post_schema = PagedPostSchema(context=posts)
        response = convert_dump(posts, paged_post_schema)
        return response, 200

    @route("/posts", methods=['POST'])
    @jwt_required
    def post(self):
        """Create a post in board"""
        data = request.data
        board_id = request.args.get('id_board', 0)
        writer_id = get_jwt_identity()  # user identity from jwt

        # Check existence of board
        board = Board.query.get_or_404(board_id)

        data['writer_id'] = writer_id
        data['board_id'] = board.id

        post_write_schema = PostWriteSchema()
        new_post = post_write_schema.load(data).data

        board.add_post(new_post)

        return '', 201

    @route('/posts/<id>', methods=['GET'])
    @jwt_required
    def get(self, id):
        """Detail a post and plus view count"""
        post = Post.query.filter(and_(Post.id == id, Post.is_published == True)).first_or_404()
        next_post = Post.query.filter(and_(Post.id > post.id, Post.board_id == post.board_id)).order_by(Post.id).first()
        prev_post = Post.query.filter(and_(Post.id < post.id, Post.board_id == post.board_id)).order_by(desc(Post.id)).first()

        post.next_post = next_post
        post.prev_post = prev_post

        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        is_user_like = post.is_user_like(user)
        post.is_user_like = is_user_like

        post.read()  # view_count +1

        post_detail_schema = PostDetailSchema()
        return convert_dump(post, post_detail_schema), 200

    @route('/posts/<id>', methods=['PATCH'])
    @jwt_required
    def patch(self, id):
        """Update a post"""
        json_data = request.get_json()
        post = Post.query.get_or_404(id)

        post_update_schema = PostUpdateSchema()
        post_update_schema.load(json_data)

        post.title = json_data['title']
        post.body = json_data['body']
        post.is_published = json_data['isPublished']

        return '', 200

    @route('/posts/<id>', methods=['DELETE'])
    @jwt_required
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
            .limit(5).all()

        posts_schema = PostSchema(many=True)
        return convert_dump(posts, posts_schema), 200

    @route('/posts/<id>/like', methods=['PATCH'])
    @jwt_required
    def like(self, id):
        """Plus 1 like count for the post"""
        post = Post.query.get_or_404(id)

        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        post.like(user)

        return '', 200

    @route('/posts/<id>/unlike', methods=['PATCH'])
    @jwt_required
    def unlike(self, id):
        """Minus 1 like count for the post"""
        post = Post.query.get_or_404(id)

        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        post.unlike(user)

        return '', 200
