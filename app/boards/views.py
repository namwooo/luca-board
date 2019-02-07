from flask import request, jsonify
from flask_classful import FlaskView, route
from flask_login import login_required, current_user
from marshmallow import ValidationError

from app import db
from app.exceptions import WriterOnly
from app.posts.models import Post
from app.posts.schemas import posts_list_schema
from .models import Board
from .schemas import BoardsSchema, BoardsUpdateSchema


class BoardsView(FlaskView):

    @route('', methods=['GET'])
    def list(self):
        """List all boards ordered by created date"""
        boards_schema = BoardsSchema(many=True)
        boards = Board.query.order_by(Board.created_at).all()

        return boards_schema.jsonify(boards), 200

    @route('', methods=['POST'])
    @login_required
    def create(self):
        """Create a board"""
        data = request.get_json()
        data['writer_id'] = current_user.id

        board_schema = BoardsSchema()
        try:
            result = board_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), 422

        new_board = result.data

        db.session.add(new_board)
        db.session.commit()

        return board_schema.jsonify(new_board), 200

    @route("/<id>", methods=['PUT'])
    @login_required
    def update(self, id):
        """Update a board"""
        data = request.get_json()
        board = Board.query.get_or_404(id)

        if not board.is_writer(current_user):
            raise WriterOnly('Writer Only: permission denied')

        boards_update_schema = BoardsUpdateSchema(context={'instance': board})

        try:
            result = boards_update_schema.load(data)
        except ValidationError as e:
            return jsonify(e.messages), 422

        db.session.commit()
        return boards_update_schema.jsonify(board), 200

    @route("/<id>", methods=['DELETE'])
    @login_required
    def delete(self, id):
        """Delete a board"""
        board = Board.query.get_or_404(id)

        if not board.is_writer(current_user):
            raise WriterOnly('Writer Only: permission denied')

        db.session.delete(board)  # integrity issue here
        db.session.commit()

        return '', 200

    @route("/<board_id>/posts", methods=['GET'])
    def post_list(self, board_id):
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
