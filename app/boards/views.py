from flask import request
from flask_classful import FlaskView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import transaction, handle_error, db
from app.exceptions import WriterOnlyException
from app.helpers import convert_dump
from app.users.models import User
from .models import Board
from .schemas import BoardSchema, BoardUpdateSchema, BoardCreateSchema


class BoardView(FlaskView):
    decorators = [transaction, handle_error]

    def index(self):
        """List all boards ordered by created date"""
        boards = Board.query.order_by(Board.created_at).all()

        boards_schema = BoardSchema(many=True)
        response = convert_dump(boards, boards_schema)
        return response, 200

    def get(self, id):
        board = Board.query.get_or_404(id)
        
        board_schema = BoardSchema()
        response = convert_dump(board, board_schema)
        return response, 200

    @jwt_required
    def post(self):
        """Create a board"""
        data = request.get_json()

        board_create_schema = BoardCreateSchema()
        new_board = board_create_schema.load(data).data

        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        user.add_board(new_board)

        return '', 201

    @jwt_required
    def patch(self, id):
        """Partial-update a board"""
        data = request.get_json()

        board = Board.query.get_or_404(id)

        user_id = get_jwt_identity()
        if not board.is_writer(user_id):
            raise WriterOnlyException()

        board_update_schema = BoardUpdateSchema()
        board_update_schema.load(data)

        board.title = data['title']

        return '', 200

    @jwt_required
    def delete(self, id):
        """Delete a board"""
        board = Board.query.get_or_404(id)

        user_id = get_jwt_identity()
        if not board.is_writer(user_id):
            raise WriterOnlyException()

        db.session.delete(board)

        return '', 200
