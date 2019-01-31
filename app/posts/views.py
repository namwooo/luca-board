from flask import jsonify, request
from flask_classful import FlaskView, route
from flask_login import current_user, login_required
from marshmallow import ValidationError
from werkzeug.exceptions import abort

from app import db
from app.boards.models import Board
from app.posts.schemas import posts_list_schema, posts_detail_schema, PostsSchema
from .models import Post


class PostsView(FlaskView):
    route_base = '/'

    @route("/boards/<board_id>/posts", methods=['GET'])
    def list(self, board_id):
        """List all published posts in board ordered by created date"""

        page = request.args.get('p', default=1, type=int)

        board = Board.query.get(board_id)
        posts = Post.query.filter(Post.board_id == board_id) \
            .filter(Post.is_published == True) \
            .order_by(Post.created_at.desc()) \
            .paginate(page=page, per_page=15, error_out=False)

        if not board:
            return jsonify({'message': 'The board does not exist'}), 404

        return posts_list_schema.jsonify(posts.items), 200

    @route("/boards/<board_id>/posts", methods=['POST'])
    @login_required
    def create(self, board_id):

        board = Board.query.get(board_id)
        if not board:
            return jsonify({'message': 'The board does not exist'}), 404

        data = request.get_json()
        data['board_id'] = board_id
        data['writer_id'] = current_user.id
        post_schema = PostsSchema()

        try:
            result = post_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), 422

        new_post = result.data

        db.session.add(new_post)
        db.session.commit()

        return post_schema.jsonify(new_post), 200

    @route("/posts/<id>", methods=['GET'])
    def detail(self, id):
        """Detail a post and plus view count"""

        post = Post.query.filter_by(id=id, is_published=True).first_or_404()

        post.view_count += 1

        db.session.add(post)
        db.session.commit()

        return posts_detail_schema.jsonify(post), 200

    @route("/posts/rank", methods=['GET'])
    def rank(self):
        """List ranked posts by its like counts"""
        posts = Post.query.filter(Post.is_published == True) \
            .order_by(Post.like_count.desc())\
            .limit(10).all()

        if not posts:
            return jsonify({'message': 'posts do not exist'}), 404

        return posts_list_schema.jsonify(posts), 200
